# RAG Pipeline — Q&A Guide

## 1. What is RAG and why does it matter?

**Q: What is Retrieval-Augmented Generation?**
RAG connects LLMs to external knowledge at query time. Instead of relying solely on training data, the model retrieves relevant documents before responding, grounding answers in source material and reducing hallucination.

**Q: Why not fine-tune?**
Fine-tuning bakes knowledge into weights — expensive, slow, requires retraining when data changes. RAG is dynamic: update documents and answers change immediately.

**Q: How does RAG compare to context stuffing?**
Pasting entire documents into prompts hits token limits and costs more. RAG retrieves only the 2-3 most relevant chunks per query.

## 2. What did you build?

**Q: What is the architecture?**
The same RAG pipeline twice. Phase 1 uses Vertex AI RAG Engine (managed). Phase 2 rebuilds every layer with ChromaDB and direct Gemini API calls.

**Q: Why build it twice?**
Understanding (learn what managed services abstract), portability (pattern works with any backend), differentiation (most candidates show one approach).

## 3. How does Vertex AI RAG Engine work?

**Q: What does create_corpus() do?**
Provisions a managed Cloud Spanner vector database. No schema or capacity configuration needed.

**Q: What does upload_file() do?**
Four operations: read, chunk, embed with text-embedding-004, store vectors in Cloud Spanner.

**Q: What does Tool.from_retrieval() do?**
Creates a Gemini tool that auto-retrieves relevant chunks and injects them into the prompt before generation.

## 4. How does ChromaDB work?

**Q: How does chunking work?**
A Python function splits documents by character count with configurable overlap. chunk_size=200 and overlap=50 produces 8 chunks from 3 documents.

**Q: What is an embedding?**
A 768-dimension vector representing semantic meaning. Similar text produces similar vectors.

**Q: How does the prompt template work?**
You build it manually: instruct Gemini to answer based ONLY on provided context, insert retrieved chunks. This is what Vertex AI builds automatically.

## 5. What were the key findings?

**Q: Were results identical?**
Yes. All four questions produced equivalent answers. Both correctly refused to hallucinate on unanswerable questions.

**Q: How were unanswerable questions handled?**
Phase 1: "sources do not contain information." Phase 2: "I don't have information about that." Neither hallucinated.

**Q: What did cross-document queries show?**
Retrieved from multiple documents and synthesized coherent answers combining PTO rates with expense limits.

## 6. What technical issues did you solve?

**Q: Region?** us-central1 blocked. Fix: europe-west1.
**Q: GCS import?** Cross-region 500 error. Fix: upload_file() direct.
**Q: SDK?** google.generativeai deprecated. Fix: google.genai.
**Q: Embedding model?** AI Studio uses gemini-embedding-001, not text-embedding-004.
**Q: Parameters?** VertexRagStore expects rag_resources not rag_corpora.

## 7. Production considerations?

**Q: What differs in production?**
Token-based chunking, persistent vector store, hybrid search, re-ranking, evaluation metrics, citation extraction, monitoring.

**Q: When Vertex AI vs ChromaDB?**
Vertex AI for production (managed, scaling, security). ChromaDB for prototyping and learning.

## 8. Portfolio context?

**Q: What gap does this fill?**
Previous projects used structured data. This is the first handling unstructured data via RAG.

## 9. Conceptual deep dives

**Q: What is cosine similarity?**
Measures angle between vectors. Similar direction = similar meaning. ChromaDB uses L2 distance by default.

**Q: Why does chunk overlap matter?**
Information at boundaries gets split. Overlap ensures complete sentences appear in at least one chunk.

**Q: How to set distance threshold?**
Tuning parameter. Evaluate against test questions with known answers.

## 10. Security considerations?

**Q: API key secure?**
Environment variable, never hardcoded. Production uses secrets manager.

**Q: Data privacy?**
Phase 2 keeps documents local. Only chunks sent to Gemini for generation.

## 11. Troubleshooting

- "text-embedding-004 not found" → Use gemini-embedding-001
- "RAG Engine restricted" → Use europe-west1
- "Policy violated for gemini-2.0-flash" → Use gemini-2.5-flash
- "500 on import_files" → Use upload_file()
- "Collection already exists" → Use get_or_create_collection()
