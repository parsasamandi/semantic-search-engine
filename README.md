# 🔍 Semantic Search Engine

AI-powered document search that understands **meaning**, not just keywords. Search "neural networks" and find documents about "deep learning" automatically.

## 🧠 How It Works

### Architecture Overview
```
Text Document → Embedding Model → 384D Vector → FAISS Index
                     ↓
User Query → Embedding Model → 384D Vector → Similarity Search → Results
```

### Step-by-Step Process

**1. Document Upload**
- User uploads `.txt` files via REST API
- FastAPI receives and validates file content

**2. Embedding Generation**
- Sentence-transformers (`all-MiniLM-L6-v2`) converts text to vectors
- Each document becomes 384 floating-point numbers
- Similar meanings = similar vector patterns

**3. Vector Indexing**
- FAISS stores vectors in IndexFlatL2 (L2 distance metric)
- Enables fast similarity search across all documents
- Rebuilds index after each upload

**4. Search Process**
- Query text converted to 384D vector using same model
- FAISS calculates L2 distance to all document vectors
- Returns top-k closest matches with similarity scores

**5. Similarity Scoring**
```python
similarity = 1 / (1 + L2_distance)
```
- Converts distance to 0-1 scale
- Higher score = more semantically similar

## 🛠️ Tech Stack

| Component | Purpose | Why This Choice |
|-----------|---------|-----------------|
| **Sentence Transformers** | Generate embeddings | Free, open-source, no API costs |
| **FAISS** | Vector search | Facebook's optimized similarity search |
| **FastAPI** | REST API | Async support, automatic validation |
| **NumPy** | Array operations | Efficient numerical computing |

## 🚀 Quick Start
```bash
# Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
python main.py

# Access
open http://localhost:8000
```

## 🔬 Technical Details

### Embedding Model
- **Model**: `all-MiniLM-L6-v2`
- **Architecture**: 6-layer MiniLM transformer
- **Output**: 384 dimensions
- **Training**: 1B+ sentence pairs
- **Size**: ~90MB

## 🚀 Deployment

Works on: Railway, Render, Heroku, AWS, GCP

**Environment**: None needed (100% free, no API keys)

---

**Built with**: FastAPI • Sentence Transformers • FAISS