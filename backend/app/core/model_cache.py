"""
Centralized model cache with warmup endpoint
Reduces cold start time by pre-loading models
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Model loading functions
_models_loaded = {
    "embeddings": False,
    "clip": False,
    "blip": False,
    "ocr": False
}

_executor = ThreadPoolExecutor(max_workers=4)

async def warmup_models():
    """Async warmup - loads models in parallel"""
    print("[INFO] Starting model warmup...")
    
    tasks = []
    
    # Load embedding model
    if not _models_loaded["embeddings"]:
        tasks.append(_executor.submit(_load_embeddings))
    
    # Load CLIP model
    if not _models_loaded["clip"]:
        tasks.append(_executor.submit(_load_clip))
    
    # Load BLIP model
    if not _models_loaded["blip"]:
        tasks.append(_executor.submit(_load_blip))
    
    # Load OCR
    if not _models_loaded["ocr"]:
        tasks.append(_executor.submit(_load_ocr))
    
    # Wait for all to complete
    for task in tasks:
        await asyncio.get_event_loop().run_in_executor(None, task.result)
    
    print("[INFO] All models warmed up!")
    return {"status": "ready", "models": _models_loaded}

def _load_embeddings():
    try:
        from app.core.embeddings.embedder import get_embedding_model
        get_embedding_model()
        _models_loaded["embeddings"] = True
        print("[INFO] ✓ Embeddings model loaded")
    except Exception as e:
        print(f"[ERROR] Failed to load embeddings: {e}")

def _load_clip():
    try:
        from app.core.embeddings.clip_embedder import load_clip_model
        load_clip_model()
        _models_loaded["clip"] = True
        print("[INFO] ✓ CLIP model loaded")
    except Exception as e:
        print(f"[ERROR] Failed to load CLIP: {e}")

def _load_blip():
    try:
        from app.core.embeddings.blip_captioner import load_blip_model
        load_blip_model()
        _models_loaded["blip"] = True
        print("[INFO] ✓ BLIP model loaded")
    except Exception as e:
        print(f"[ERROR] Failed to load BLIP: {e}")

def _load_ocr():
    try:
        from app.core.embeddings.ocr_reader import get_ocr_reader
        get_ocr_reader()
        _models_loaded["ocr"] = True
        print("[INFO] ✓ OCR reader loaded")
    except Exception as e:
        print(f"[ERROR] Failed to load OCR: {e}")

def get_models_status():
    """Check which models are loaded"""
    return _models_loaded
