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

if __name__ == "__main__":
    col = chromadb.Client().create_collection("acme_kb")
    for doc in load_documents("../docs"):
        for i, chunk in enumerate(chunk_text(doc["text"])):
            col.add(ids=[f"{doc['filename']}_chunk_{i}"], embeddings=[get_embedding(chunk)], documents=[chunk], metadatas=[{"source": doc["filename"]}])
    print("=" * 60)
    print("STEP 4: RETRIEVAL")
    print("=" * 60)
    print(f"Vector store: {col.count()} chunks")
    for q in ["How many PTO days for a 4-year employee?", "What is the meal limit for international travel?", "What are the password requirements?", "What is the parental leave policy?"]:
        print(f"\n  Q: {q}")
        r = col.query(query_embeddings=[get_embedding(q)], n_results=2)
        for i in range(len(r["ids"][0])):
            print(f"    {r['ids'][0][i]}  dist={r['distances'][0][i]:.4f}")
