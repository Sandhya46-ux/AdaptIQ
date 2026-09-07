Adaptive Learning Intelligence Platform

RAG:

Implemented rag/ingest.py for chunking markdown/text documents and saving embeddings to ChromaDB.

Built rag/retrieval/retrieval.py for semantic similarity search using all-MiniLM-L6-v2.

Created rag/retrieval/generator.py to formulate grounded prompts and return structured JSON context/answers.

How to Test:

Activate venv and run pip install -r requirements.txt.

Run python rag/ingest.py (verify rag/embeddings/ populates).

Run python rag/retrieval/generator.py (verify retrieved context output).