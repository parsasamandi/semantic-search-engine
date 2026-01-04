# 🚀 QUICK START GUIDE

## ⚡ Get Running in 5 Minutes

### Step 1: Set Up (2 minutes)

```bash
# Navigate to project
cd semantic-search-engine

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure OpenAI API (1 minute)

1. Get your API key: https://platform.openai.com/api-keys
2. Create `.env` file:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 3: Run (30 seconds)

```bash
python main.py
```

Open: http://localhost:8000

### Step 4: Test (1.5 minutes)

1. Upload the 6 sample documents from `sample_documents/` folder
2. Try these searches:
   - "machine learning and neural networks"
   - "web frameworks and APIs"
   - "database management"
   - "AWS and Docker"

---

## 📊 Expected Results

When you search "machine learning", you should see:
1. **artificial_intelligence.txt** - High similarity (~85-95%)
2. **python_programming.txt** - Medium similarity (~60-75%)
3. Other docs with lower scores

The system uses semantic understanding, so it finds conceptually similar content, not just keyword matches!

---

## 🧪 Testing Commands

```bash
# Test upload
curl -X POST "http://localhost:8000/upload" \
  -F "file=@sample_documents/artificial_intelligence.txt"

# Test search
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning algorithms", "top_k": 3}'

# Check stats
curl "http://localhost:8000/stats"
```

---

## ✅ Success Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` file created with API key
- [ ] Server running on port 8000
- [ ] Can access http://localhost:8000
- [ ] Uploaded 5+ documents
- [ ] Search returns relevant results
- [ ] Similarity scores showing

---

## 🐛 Quick Troubleshooting

**"Module not found" errors:**
```bash
pip install -r requirements.txt --upgrade
```

**"OpenAI API error":**
- Check your `.env` file exists
- Verify API key is correct
- Restart the server

**"No documents uploaded":**
- Make sure files are `.txt` format
- Check file is not empty
- Try uploading one file at a time

---

## 🎯 Next Steps

Once it's working:

1. **Customize**: Modify the UI colors and styling
2. **Expand**: Add more document types (PDF support)
3. **Deploy**: Follow Railway/Render deployment guide in README
4. **Enhance**: Add user authentication
5. **Scale**: Implement document categories

---

## 💡 Understanding the Results

**Similarity Scores Explained:**
- **90-100%**: Nearly identical content
- **70-90%**: Highly relevant, same topic
- **50-70%**: Related concepts
- **Below 50%**: Tangentially related

The system uses **L2 distance** converted to similarity:
```
similarity = 1 / (1 + distance)
```

Shorter distances = higher similarity!

---

## 📸 Screenshots

After uploading documents, you should see:
- Document counter showing 6 documents
- List of uploaded files
- Active search box
- Clean, modern interface

After searching, expect:
- Top 3 results ranked
- Similarity percentages
- Document previews
- Document names

---

## 🎓 What You've Built

You now have a working:
- ✅ Vector database (FAISS)
- ✅ Embedding generation pipeline
- ✅ RESTful API
- ✅ Modern web interface
- ✅ Production-ready architecture

This is the foundation for:
- Document management systems
- Knowledge bases
- Content recommendation engines
- Semantic wikis
- Research tools

---

Ready to deploy? Check the **Deployment** section in README.md!
