# Architecture Document — RAG Pipeline

## Overview

This project implements the same RAG pipeline using two backends: Google Vertex AI RAG Engine (managed) and ChromaDB (self-built).

## Architecture Decision Records

### ADR-1: Two-Phase Approach

**Decision:** Build the same pipeline twice.
**Rationale:** Proves the pattern is portable and develops deep understanding of managed service abstractions.

### ADR-2: ChromaDB as Self-Built Vector Store

**Decision:** Use ChromaDB instead of FAISS, Pinecone, or Vertex AI Vector Search.
**Rationale:** Runs in-process, no servers, no cost, simple API.

### ADR-3: Google AI Studio API for Phase 2

**Decision:** Use free API key instead of Vertex AI for Phase 2.
**Rationale:** Eliminates sandbox token limits. Uses current google.genai SDK.

### ADR-4: Small Synthetic Documents

**Decision:** Use 3 small documents (~40 words each).
**Rationale:** Stays within sandbox token limits while demonstrating all RAG behaviors.

### ADR-5: europe-west1 Region

**Decision:** Deploy to europe-west1 instead of us-central1.
**Rationale:** Google restricted RAG Engine in us-central1/us-east1/us-east4 for new projects.

### ADR-6: Direct File Upload vs GCS Import

**Decision:** Use rag.upload_file() instead of rag.import_files().
**Rationale:** GCS cross-region import returned 500 errors.

### ADR-7: Character-Based Chunking

**Decision:** Use character-count chunking in Phase 2.
**Rationale:** Simplest to implement. Production would use token-based.

### ADR-8: In-Memory ChromaDB

**Decision:** Use in-memory mode rather than persistent storage.
**Rationale:** Acceptable for demo with 3 small documents.

## RAG Pipeline Flow

```
                Phase 1 (Vertex AI)          Phase 2 (ChromaDB)
1. LOAD DOCS     GCS bucket                   Local filesystem
2. CHUNK          Automatic (ChunkingConfig)   chunk_text() custom
3. EMBED          text-embedding-004 (auto)    gemini-embedding-001 (explicit)
4. STORE          Cloud Spanner (managed)      ChromaDB (in-memory)
5. RETRIEVE       rag.retrieval_query()        collection.query()
6. GENERATE       Gemini + Tool.from_retrieval Gemini + custom prompt
```

## Distance Scores (Phase 2)

| Query | Top Chunk | Distance | Correct? |
|-------|-----------|----------|----------|
| PTO for 4 years? | pto_policy.txt | 0.5604 | Yes |
| Meal limit? | expense_policy.txt | 0.6912 | Yes |
| Passwords? | security_policy.txt | 0.7019 | Yes |
| Parental leave? | pto_policy.txt | 0.7351 | Correct fallback |

## Production Considerations

| Concern | This Project | Production |
|---------|-------------|------------|
| Chunking | Character-based | Token-based, sentence-aware |
| Vector DB | In-memory ChromaDB | Persistent, scaled |
| Retrieval | Top-k only | Re-ranking, hybrid search |
| Evaluation | Manual | Automated RAG eval |
| Monitoring | None | Latency, quality metrics |
