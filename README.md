# 🔍 Semantic Search Engine

An AI-powered document search engine using OpenAI embeddings and FAISS for vector similarity search. Upload text documents and search them using natural language queries.

## 🌟 Features

- **Upload multiple text documents** (.txt format)
- **Generate AI embeddings** using OpenAI's text-embedding-3-small model
- **Vector similarity search** powered by FAISS
- **Real-time search results** with similarity scores
- **Clean, modern UI** with drag-and-drop support
- **RESTful API** built with FastAPI

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **AI/ML**: OpenAI Embeddings API, FAISS (Facebook AI Similarity Search)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Deployment**: Railway / Render compatible

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd semantic-search-engine
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 5. Run the Application

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

## 📝 Usage Guide

### Uploading Documents

1. Click the upload area or drag and drop `.txt` files
2. Upload at least 5 documents for best results
3. Wait for the "uploaded successfully" message
4. Documents are immediately available for searching

### Searching

1. Once documents are uploaded, the search box becomes active
2. Enter a natural language query (e.g., "machine learning algorithms")
3. Click "Search" or press Enter
4. View top 3 most similar documents with similarity scores

### Sample Documents

Create these sample `.txt` files to test the system:

**ai_basics.txt**:
```
Artificial Intelligence is the simulation of human intelligence by machines. 
It includes machine learning, deep learning, and neural networks.
```

**python_programming.txt**:
```
Python is a high-level programming language known for its simplicity and readability.
It's widely used in web development, data science, and AI applications.
```

**web_development.txt**:
```
Web development involves building websites and web applications using HTML, CSS, and JavaScript.
Modern frameworks like React and Vue make development more efficient.
```

**database_systems.txt**:
```
Databases store and organize data for efficient retrieval. SQL databases like MySQL and PostgreSQL
are relational, while MongoDB is a popular NoSQL option.
```

**cloud_computing.txt**:
```
Cloud computing provides on-demand access to computing resources over the internet.
Major providers include AWS, Google Cloud, and Microsoft Azure.
```

## 🔌 API Documentation

### Upload Document
```http
POST /upload
Content-Type: multipart/form-data

Response:
{
  "status": "success",
  "filename": "document.txt",
  "total_documents": 5,
  "document_length": 1234
}
```

### Search Documents
```http
POST /search
Content-Type: application/json

{
  "query": "your search query",
  "top_k": 3
}

Response:
[
  {
    "document_name": "document.txt",
    "content_preview": "First 200 characters...",
    "similarity_score": 0.8534,
    "rank": 1
  }
]
```

### Get Statistics
```http
GET /stats

Response:
{
  "total_documents": 5,
  "document_names": ["doc1.txt", "doc2.txt"],
  "index_ready": true
}
```

### Clear All Documents
```http
DELETE /clear

Response:
{
  "status": "cleared",
  "total_documents": 0
}
```

## 🌐 Deployment

### Deploy to Railway

1. Create account at [Railway.app](https://railway.app)
2. Install Railway CLI:
```bash
npm install -g @railway/cli
```

3. Login and initialize:
```bash
railway login
railway init
```

4. Add environment variable:
```bash
railway variables set OPENAI_API_KEY=your-key-here
```

5. Deploy:
```bash
railway up
```

### Deploy to Render

1. Create account at [Render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy

## 💰 Cost Estimation

### OpenAI API Costs (as of 2024)

**text-embedding-3-small**: $0.00002 per 1K tokens

Example usage:
- 10 documents (avg 500 words each): ~$0.0014
- 100 searches: ~$0.002
- **Monthly estimate for moderate use**: $1-5

### Deployment Costs

- **Railway**: Free tier available, $5/month for starter
- **Render**: Free tier available (with limitations)

## 🧪 Testing

Test the API endpoints:

```bash
# Upload a document
curl -X POST "http://localhost:8000/upload" \
  -F "file=@test_document.txt"

# Search
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence", "top_k": 3}'

# Get stats
curl "http://localhost:8000/stats"
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'faiss'"
```bash
pip install faiss-cpu
```

### "OpenAI API key not found"
- Make sure `.env` file exists and contains `OPENAI_API_KEY`
- Restart the application after adding the key

### "No documents uploaded yet"
- Upload at least one document before searching
- Check the file is `.txt` format and not empty

### FAISS index errors
- Ensure all documents are text-based (UTF-8 encoding)
- Try clearing all documents and re-uploading

## 📚 How It Works

1. **Document Upload**: User uploads text files
2. **Embedding Generation**: OpenAI API converts text to 1536-dimensional vectors
3. **Vector Storage**: FAISS indexes these vectors for fast similarity search
4. **Search Query**: User query is converted to embedding
5. **Similarity Search**: FAISS finds the closest vectors using L2 distance
6. **Results**: Top matches are returned with similarity scores

## 🔐 Security Notes

- Never commit `.env` file or API keys to Git
- Use environment variables for sensitive data
- Consider rate limiting for production use
- Validate file uploads (size, type, content)

## 📈 Future Enhancements

- [ ] Support for PDF and DOCX files
- [ ] Persistent storage (database integration)
- [ ] User authentication
- [ ] Advanced filtering options
- [ ] Batch document upload
- [ ] Export search results
- [ ] Document categorization
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙋 Support

For issues or questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review OpenAI and FAISS documentation

## ✅ Success Criteria Checklist

- [x] Works with 5+ documents
- [x] Search returns relevant results
- [x] Similarity scores displayed
- [x] Clean, functional UI
- [x] RESTful API endpoints
- [x] Deployment-ready
- [x] Comprehensive documentation

---

Built with ❤️ using FastAPI, OpenAI, and FAISS
