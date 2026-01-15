from app.core.embeddings.clip_embedder import embed_text_clip
from app.core.vectorstore.vector_store import init_index, IMAGE_INDEX_NAME


def retrieve_images(query, top_k=5):
    query_embedding = embed_text_clip(query)

    index = init_index(
        IMAGE_INDEX_NAME,
        len(query_embedding)
    )


    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    retrieved = []
    for match in results.get("matches", []):
        metadata = match.get("metadata", {})

        retrieved.append({
            "score": match.get("score", 0),
            "source": metadata.get("source", "UNKNOWN_IMAGE"),
            "type": metadata.get("type", "image")
        })

    return retrieved
