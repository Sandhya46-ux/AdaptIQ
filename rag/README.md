# AdaptIQ - Grounded AI Knowledge Layer (`rag/`)

This directory implements Retrieval-Augmented Generation (RAG) to power the AI Tutor with grounded educational content[cite: 3, 4].

## Directory Structure
* `documents/`: Raw curated educational text files.
* `embeddings/`: Local ChromaDB vector database[cite: 3].
* `retrieval/`: Semantic search engine (`retrieval.py`) and prompt generator (`generator.py`)[cite: 3].
* `ingest.py`: Document loader and vector store generation script[cite: 3].

## Usage for Backend Integration
Import `generate_grounded_answer` in `backend/routers/tutor.py`:

```python
from rag.retrieval.generator import generate_grounded_answer

# Call RAG pipeline
response = generate_grounded_answer("How do I solve a quadratic equation?")
# Returns dict: {"query": ..., "context_used": ..., "answer": ...}