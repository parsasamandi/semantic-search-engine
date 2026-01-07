from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List

app = FastAPI(title="Semantic Search Engine")

# Initialize FREE embedding model (no API key needed!)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage
documents = []
document_names = []
embeddings = []
index = None

class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

class SearchResult(BaseModel):
    document_name: str
    content_preview: str
    similarity_score: float
    rank: int

def get_embedding(text: str) -> List[float]:
    """Generate embedding for text using Hugging Face (FREE!)"""
    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {str(e)}")

def rebuild_index():
    """Rebuild FAISS index with current embeddings"""
    global index
    if len(embeddings) == 0:
        index = None
        return
    
    embeddings_array = np.array(embeddings, dtype='float32')
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_array)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/upload")
async def upload_document(file: UploadFile):
    """Upload and process a document"""
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    
    try:
        # Read file content
        content = await file.read()
        text = content.decode('utf-8')
        
        if len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Generate embedding
        embedding = get_embedding(text)
        
        # Store document
        documents.append(text)
        document_names.append(file.filename)
        embeddings.append(embedding)
        
        # Rebuild index
        rebuild_index()
        
        return {
            "status": "success",
            "filename": file.filename,
            "total_documents": len(documents),
            "document_length": len(text)
        }
    
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding not supported. Please use UTF-8.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/search", response_model=List[SearchResult])
async def search_documents(query: SearchQuery):
    """Search for similar documents"""
    if index is None or len(documents) == 0:
        raise HTTPException(status_code=400, detail="No documents uploaded yet")
    
    try:
        # Generate query embedding
        query_embedding = np.array([get_embedding(query.query)], dtype='float32')
        
        # Search using FAISS
        k = min(query.top_k, len(documents))
        distances, indices = index.search(query_embedding, k)
        
        # Format results
        results = []
        for rank, (idx, distance) in enumerate(zip(indices[0], distances[0]), 1):
            # Convert L2 distance to similarity score (0-1)
            similarity = 1 / (1 + distance)
            
            results.append(SearchResult(
                document_name=document_names[idx],
                content_preview=documents[idx][:200] + "..." if len(documents[idx]) > 200 else documents[idx],
                similarity_score=round(similarity, 4),
                rank=rank
            ))
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get current system statistics"""
    return {
        "total_documents": len(documents),
        "document_names": document_names,
        "index_ready": index is not None
    }

@app.delete("/clear")
async def clear_documents():
    """Clear all documents and reset the index"""
    global documents, document_names, embeddings, index
    documents = []
    document_names = []
    embeddings = []
    index = None
    
    return {"status": "cleared", "total_documents": 0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)