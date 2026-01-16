"""
Batch processing utilities for efficient embedding generation
"""

def batch_embed_documents(chunks: list, batch_size: int = 32):
    """
    Process documents in batches to reduce memory usage
    and improve throughput
    """
    from app.core.embeddings.embedder import get_embedding_model
    
    model = get_embedding_model()
    all_embeddings = []
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        embeddings = model.embed_documents(batch)
        all_embeddings.extend(embeddings)
        print(f"[INFO] Processed batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
    
    return all_embeddings
