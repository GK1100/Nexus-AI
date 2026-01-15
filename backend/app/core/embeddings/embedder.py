# embedder.py — LANGCHAIN VERSION (FINAL)

from langchain_huggingface import HuggingFaceEmbeddings
import time

import os
os.environ["HF_HOME"] = "/tmp/huggingface"

# Global variable for lazy loading
_embedding_model = None

def get_embedding_model():
    """Lazy load embedding model on first use (singleton pattern)"""
    global _embedding_model
    
    if _embedding_model is not None:
        return _embedding_model
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[INFO] Loading embedding model (attempt {attempt + 1}/{max_retries})...")
            _embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                # model_name="BAAI/bge-large-en",
                model_kwargs={"device": "cpu"},  # set "cuda" if gpu available
                encode_kwargs={"normalize_embeddings": True}
            )
            print("[INFO] Embedding model loaded successfully!")
            return _embedding_model
        except Exception as e:
            print(f"[ERROR] Failed to load embedding model (attempt {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"[INFO] Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("[ERROR] All retry attempts failed!")
                raise Exception(f"Failed to load embedding model after {max_retries} attempts: {str(e)}")

def embed_query(text: str):
    model = get_embedding_model()  # Load only when called
    return model.embed_query(text)

def embed_documents(chunks: list):
    model = get_embedding_model()  # Load only when called
    return model.embed_documents(chunks)
