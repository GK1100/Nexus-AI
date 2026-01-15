# 🧠 Multimodal RAG – Universal Document & Image Intelligence

A production-ready **Multimodal Retrieval-Augmented Generation (RAG)** system for querying **documents and images** using natural language.  
Supports **text + vision retrieval** with grounded LLM answers.

---

## ✨ Features

- 📄 Document Q&A (PDF, DOCX, TXT)
- 🖼️ Image Understanding (OCR + Captioning + Embeddings)
- 🔍 Multimodal Retrieval (Text + Image vectors)
- 🤖 LLM-grounded answers (no hallucinations)
- 🌐 Clean Web UI (upload + chat)
- 🚀 Dockerized full-stack setup
- 🧩 Session-based isolation

---

## 🏗️ Architecture

Frontend (HTML / CSS / JS)

↓

FastAPI Backend

↓

Text → BGE Embeddings
Images → CLIP + OCR + BLIP

↓

Pinecone Vector DB

↓

Groq LLaMA-3

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- LangChain
- Pinecone
- Groq (LLaMA-3.1)
- HuggingFace Transformers
- CLIP, BLIP, EasyOCR

### Frontend
- HTML, CSS, Vanilla JavaScript
- Markdown rendering
- Glassmorphism UI

### DevOps
- Docker
- Docker Compose

---

## 📂 Supported File Types

| Type | Formats |
|----|----|
| Documents | PDF, DOCX, TXT |
| Images | PNG, JPG, JPEG, WEBP |

---

## 🚀 Quick Start

### 1️⃣ Clone Repository
```bash
git clone https://github.com/GK1100/Nexus-AI.git
cd Nexus-AI
```

### 2️⃣ Environment Variables
Create .env in backend root:
```bash
.env

PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_region
GROQ_API_KEY=your_groq_key
```

### 3️⃣ Run with Docker (Recommended)
```bash
docker-compose up --build
Frontend → http://localhost:3000

Backend → http://localhost:8000

Health → http://localhost:8000/health
```

### 4️⃣ Run Without Docker (Local)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
---

### 🔌 API Endpoints

POST /ingest/file – Upload document/image

POST /query – Ask questions

GET /health – Service status

---

### 🧪 Use Cases
Research paper analysis

Medical image Q&A

Business document intelligence

Diagram explanation

Knowledge base chatbot

---

### 🧩 Project Structure

├── app/

│   ├── core/
   
│   ├── services/

│   ├── routes/

│   └── main.py

├── frontend/

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

└── README.md
---

### 📌 Roadmap
Authentication

Streaming responses

RAG evaluation (RAGAS)

Hybrid search (BM25 + Vector)

---

### 📜 License
MIT License

### 👨‍💻 Author

Gaurav Kumavat

Multimodal AI | RAG | Backend Systems
