# Phase 1: Vertex AI RAG Engine

Uses Google's fully managed RAG Engine.

## Requirements
- GCP project with Vertex AI API enabled
- Region: europe-west1
- pip install google-cloud-aiplatform

## Run
```bash
python rag_lean.py
```

## What Vertex AI Manages
1. Chunking on upload
2. Embedding via text-embedding-004
3. Vector storage in Cloud Spanner
4. Similarity search
5. Context injection into Gemini prompts
