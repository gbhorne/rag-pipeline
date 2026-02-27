# I Built the Same RAG Pipeline Twice

I built the exact same RAG pipeline twice: once with Google Vertex AI RAG Engine, once from scratch with ChromaDB.

The results were identical. The code was completely different. That is the point.

Vertex AI handles everything in a few API calls. ChromaDB requires you to build every layer. Both returned the same answers. Both correctly refused to hallucinate.

The most revealing step was generation. I wrote the prompt template myself: "Answer based ONLY on the provided context." That is what Vertex AI builds behind the scenes. No magic.

Documents → Chunk → Embed → Store → Retrieve → Generate. This flow does not change regardless of backend.

Code on GitHub: [link]
