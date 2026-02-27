import chromadb
from google import genai
import os
client_ai = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def load_documents(doc_dir):
    docs = []
    for fn in sorted(os.listdir(doc_dir)):
        if fn.endswith(".txt"):
            with open(os.path.join(doc_dir, fn)) as f:
                docs.append({"filename": fn, "text": f.read()})
    return docs

def chunk_text(text, sz=200, ov=50):
    chunks, start = [], 0
    while start < len(text):
        c = text[start:start+sz].strip()
        if c: chunks.append(c)
        start += sz - ov
    return chunks

def get_embedding(text):
    return client_ai.models.embed_content(model="gemini-embedding-001", contents=text).embeddings[0].values

def retrieve(col, query, top_k=2):
    return col.query(query_embeddings=[get_embedding(query)], n_results=top_k)

def generate_answer(col, query):
    results = retrieve(col, query)
    ctx, sources = [], []
    for i in range(len(results["ids"][0])):
        src = results["metadatas"][0][i]["source"]
        ctx.append("[From " + src + "]: " + results["documents"][0][i])
        sources.append(src)
    context = "\n\n".join(ctx)
    prompt = "Answer the question based ONLY on the provided context.\n"
    prompt += 'If the context does not contain enough information, say "I don' + "'" + 't have information about that in the available documents."\n\n'
    prompt += "Context:\n" + context + "\n\nQuestion: " + query + "\n\nAnswer:"
    resp = client_ai.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"answer": resp.text, "sources": list(set(sources)), "prompt_length": len(prompt)}

if __name__ == "__main__":
    col = chromadb.Client().create_collection("acme_kb")
    for doc in load_documents("../docs"):
        for i, chunk in enumerate(chunk_text(doc["text"])):
            col.add(ids=[doc["filename"] + "_chunk_" + str(i)], embeddings=[get_embedding(chunk)], documents=[chunk], metadatas=[{"source": doc["filename"]}])
    print("=" * 60)
    print("STEP 5: GENERATION -- Complete RAG Pipeline")
    print("=" * 60)
    print("\n  Vector store: " + str(col.count()) + " chunks loaded")
    for q in ["How many PTO days for a 4-year employee?", "What is the daily meal limit for international travel?", "What are the password requirements?", "What is the parental leave policy?"]:
        print("\n  Q: " + q)
        r = generate_answer(col, q)
        print("  A: " + r["answer"])
        print("  Sources: " + ", ".join(r["sources"]))
        print("  Prompt length: " + str(r["prompt_length"]) + " chars\n")
    print("=" * 60)
    print("PHASE 2 COMPLETE -- Full RAG Pipeline with ChromaDB")
    print("=" * 60)
    print("\nWhat YOU built:")
    print("  1. Chunking     -- split documents into overlapping pieces")
    print("  2. Embedding    -- converted text to vectors (gemini-embedding-001)")
    print("  3. Vector Store -- stored vectors in ChromaDB")
    print("  4. Retrieval    -- similarity search to find relevant chunks")
    print("  5. Generation   -- built grounded prompt, called Gemini")
    print("\nWhat Vertex AI did in Phase 1 (same steps, managed):")
    print("  1. ChunkingConfig     -> automatic chunking on upload")
    print("  2. text-embedding-004 -> automatic embedding on upload")
    print("  3. Cloud Spanner      -> managed vector database")
    print("  4. retrieval_query()  -> managed similarity search")
    print("  5. Tool.from_retrieval -> automatic prompt building")
    print("\nTHE RAG PATTERN IS THE SAME.")
    print("Only the infrastructure layer changed.")
