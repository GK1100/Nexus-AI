from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ingest, query
from app.core.model_cache import warmup_models, get_models_status

app = FastAPI(title="Multimodal RAG Backend")

@app.on_event("startup")
async def startup_event():
    print("[INFO] ========================================")
    print("[INFO] Multimodal RAG Backend Starting...")
    print("[INFO] Models will load lazily on first use")
    print("[INFO] Use /warmup endpoint to pre-load models")
    print("[INFO] ========================================")

@app.get("/")
def root():
    return {"message": "Multimodal RAG Backend is running"}

# ✅ CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for dev)
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(query.router, prefix="/query", tags=["Query"])

@app.get("/health")
def health():
    """Health check endpoint - lightweight, no model loading"""
    return {"status": "ok", "message": "Server is running. Models load on first request."}

@app.get("/warmup")
async def warmup():
    """Pre-load all models to reduce first request latency"""
    result = await warmup_models()
    return result

@app.get("/models/status")
def models_status():
    """Check which models are currently loaded"""
    return get_models_status()
