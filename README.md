# Semantic Search Engine

AI-powered document search that understands meaning, not just keywords.

## How It Works

Documents and queries are converted to 384-dimensional vectors using Sentence Transformers (`all-MiniLM-L6-v2`). FAISS performs fast similarity search to find semantically related documents.

## Tech Stack

- **Sentence Transformers** - Generate text embeddings
- **FAISS** - Vector similarity search
- **FastAPI** - REST API framework
- **NumPy** - Numerical operations

## Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python main.py

# Access at http://localhost:8000
```

## Deployment

Works on Railway, Render, Heroku, AWS, and GCP. No API keys or environment variables required.