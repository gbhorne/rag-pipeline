# I Built the Same RAG Pipeline Twice to Prove a Point

RAG is the most in-demand AI pattern in production. I built the same pipeline twice: Vertex AI RAG Engine (managed) and ChromaDB (self-built). Same documents, same questions, identical results.

## Phase 1: Vertex AI

Five API calls handle everything. The GCP console showed Cloud Spanner running behind the scenes — infrastructure I never configured. Experiments proved cross-document synthesis, honest handling of unanswerable questions, and immediate searchability of new documents.

## Phase 2: ChromaDB

I rebuilt every layer: chunking function, explicit embedding calls producing 768-dim vectors, ChromaDB storage, similarity search with visible distance scores, and a custom prompt template. The prompt was the reveal — that is what Vertex AI constructs automatically.

## Results

| Question | Phase 1 | Phase 2 |
|----------|---------|---------|
| PTO for 4 years? | 20 days/year | 20 days/year |
| Meal limit? | 100/day | 100/day |
| Passwords? | All 5 criteria | All 5 criteria |
| Parental leave? | Not in sources | No information |

## The Pattern

Documents → Chunk → Embed → Store → Retrieve → Generate. Swap any component and the pattern holds.

*The best way to understand a managed service is to build what it manages.*
