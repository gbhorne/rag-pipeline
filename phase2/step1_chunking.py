import os

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

if __name__ == "__main__":
    print("=" * 60)
    print("STEP 1: CHUNKING")
    print("=" * 60)
    docs = load_documents("../docs")
    for doc in docs:
        chunks = chunk_text(doc["text"])
        print(f"  {doc['filename']} -> {len(chunks)} chunks")
        for i, c in enumerate(chunks):
            print(f"    Chunk {i}: {c[:80]}...")
