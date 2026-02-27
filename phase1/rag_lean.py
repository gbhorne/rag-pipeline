from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
import vertexai, time, glob

PROJECT_ID = "your-project-id"
LOCATION = "europe-west1"

print("\n>>> Initializing Vertex AI...")
vertexai.init(project=PROJECT_ID, location=LOCATION)

print("\n>>> Creating RAG Corpus...")
corpus = rag.create_corpus(
    display_name="acme_kb_lean",
    backend_config=rag.RagVectorDbConfig(
        rag_embedding_model_config=rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model="publishers/google/models/text-embedding-004"))))
print(f"  Corpus: {corpus.name}")

print("\n>>> Uploading documents...")
for f in sorted(glob.glob("../docs/*.txt")):
    name = f.split("/")[-1]
    rag.upload_file(corpus_name=corpus.name, path=f, display_name=name)
    print(f"  Uploaded: {name}")
time.sleep(15)
print(f"  Total files: {len(list(rag.list_files(corpus_name=corpus.name)))}")

print("\n>>> Retrieval test...")
query = "How many PTO days for a 4-year employee?"
resp = rag.retrieval_query(rag_resources=[rag.RagResource(rag_corpus=corpus.name)], text=query,
    rag_retrieval_config=rag.RagRetrievalConfig(top_k=2, filter=rag.utils.resources.Filter(vector_distance_threshold=0.5)))
print(f"  Query: {query}")
if resp.contexts and resp.contexts.contexts:
    for i, c in enumerate(resp.contexts.contexts):
        print(f"  Chunk {i+1} [{c.source_uri}]: {c.text[:150]}...")

print("\n>>> Grounded generation with Gemini...")
tool = Tool.from_retrieval(retrieval=rag.Retrieval(source=rag.VertexRagStore(
    rag_resources=[rag.RagResource(rag_corpus=corpus.name)])))
model = GenerativeModel(model_name="gemini-2.5-flash", tools=[tool])
for q in ["How many PTO days for a 4-year employee?", "What is the daily meal limit for international travel?", "What are the password requirements?"]:
    print(f"\n  Q: {q}")
    try: print(f"  A: {model.generate_content(q).text}")
    except Exception as e: print(f"  ERROR: {e}")

print("\n>>> Cleanup...")
rag.delete_corpus(name=corpus.name)
print("  Corpus deleted.\n>>> DONE")
