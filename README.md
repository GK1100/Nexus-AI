🧠 Multimodal RAG – Universal Document & Image Intelligence

A production-ready Multimodal Retrieval-Augmented Generation (RAG) system that allows users to upload documents and images and ask natural language questions.
The system intelligently retrieves relevant text + image context and generates accurate answers using modern LLMs, vision models, and vector databases.

✨ Features

📄 Document Understanding (PDF, DOCX, TXT)

🖼️ Image Understanding (OCR + Captioning + Visual Embeddings)

🔍 Multimodal Retrieval (Text + Image vectors)

🤖 LLM-powered Answers (context-grounded, no hallucinations)

🌐 Modern Web UI (drag-and-drop uploads, chat interface)

🚀 Dockerized Full-Stack Setup

🧩 Session-based Knowledge Isolation

🏗️ Architecture Overview
Frontend (HTML/CSS/JS)
        ↓
FastAPI Backend
        ↓
 ┌───────────────┐
 │  Text Docs    │ → BGE Embeddings
 │  Images       │ → CLIP Embeddings
 │  OCR + BLIP   │ → Text Embeddings
 └───────────────┘
        ↓
Pinecone Vector DB
        ↓
Groq LLM (LLaMA 3)

🛠️ Tech Stack
Backend

FastAPI

LangChain

Pinecone (Vector Database)

Groq (LLaMA-3.1)

HuggingFace Transformers

CLIP (Image Embeddings)

BLIP (Image Captioning)

EasyOCR

Frontend

HTML, CSS, Vanilla JavaScript

Markdown Rendering

Glassmorphism UI

DevOps

Docker

Docker Compose

📂 Supported File Types
Type	Formats
Documents	PDF, DOCX, TXT
Images	PNG, JPG, JPEG, WEBP
🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/your-username/multimodal-rag.git
cd multimodal-rag

2️⃣ Environment Variables

Create a .env file in the backend root:

PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_region
GROQ_API_KEY=your_groq_key

3️⃣ Run with Docker (Recommended)
docker-compose up --build


Frontend → http://localhost:3000

Backend → http://localhost:8000

Health Check → http://localhost:8000/health

4️⃣ Run Without Docker (Local Dev)
Backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend

Open index.html directly in the browser
(or use Live Server)

📥 How It Works
Ingestion

Upload document or image

Text is chunked and embedded

Images use:

CLIP → visual embeddings

OCR → extracted text

BLIP → captions

Stored in Pinecone with session isolation

Querying

User asks a question

Relevant chunks + images retrieved

Context passed to LLM

Grounded answer returned

🔌 API Endpoints
Upload File
POST /ingest/file

Ask Question
POST /query

{
  "question": "What is explained in the diagram?",
  "session_id": "uuid"
}

Health Check
GET /health

🧪 Example Use Cases

Research paper analysis

Medical image understanding

Business document Q&A

Technical diagram explanation

Knowledge base chatbot

🧩 Project Structure
├── app/
│   ├── core/
│   │   ├── embeddings/
│   │   ├── retriever/
│   │   ├── vectorstore/
│   │   └── preprocess/
│   ├── services/
│   ├── routes/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

⚠️ Notes

Free Pinecone & Groq tiers supported

Designed for scalable production use

No hallucinations — answers strictly from retrieved context

📌 Future Improvements

Authentication & user accounts

Streaming responses

RAG evaluation (RAGAS)

Hybrid search (BM25 + Vector)

Cloud deployment (Railway / Render)

📜 License

MIT License – free to use, modify, and distribute.

👨‍💻 Author

Gaurav Kumavat
Multimodal AI | RAG | Backend Systems