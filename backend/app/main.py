from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ingest, query

app = FastAPI(title="Multimodal RAG Backend")

@app.on_event("startup")
async def startup_event():
    print("[INFO] ========================================")
    print("[INFO] Multimodal RAG Backend Starting...")
    print("[INFO] Models will load lazily on first use")
    print("[INFO] ========================================")

@app.get("/")
def root():
    return {"message": "Multimodal RAG Backend is running"}

# ✅ CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(query.router, prefix="/query", tags=["Query"])

@app.get("/health")
def health():
    return {"status": "ok"}
