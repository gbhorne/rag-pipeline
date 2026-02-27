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
    print("=" * 60)
    print("STEP 3: VECTOR STORE")
    print("=" * 60)
    col = chromadb.Client().create_collection("acme_kb")
    for doc in load_documents("../docs"):
        for i, chunk in enumerate(chunk_text(doc["text"])):
            emb = get_embedding(chunk)
            col.add(ids=[f"{doc['filename']}_chunk_{i}"], embeddings=[emb], documents=[chunk], metadatas=[{"source": doc["filename"]}])
            print(f"  Stored: {doc['filename']}_chunk_{i} ({len(emb)} dims)")
    print(f"Total vectors: {col.count()}")
