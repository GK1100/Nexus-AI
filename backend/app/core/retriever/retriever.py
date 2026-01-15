from app.core.embeddings.embedder import embed_query
from app.core.vectorstore.vector_store import init_index, TEXT_INDEX_NAME


def retrieve_chunks(query_text, top_k=5, filter=None):
    query_embedding = embed_query(query_text)

    index = init_index(
        name=TEXT_INDEX_NAME,
        dimension=len(query_embedding)
    )

    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter
    )

    retrieved = []
    for match in result.get("matches", []):
        retrieved.append({
            "score": match.get("score", 0),
            "text": match.get("metadata", {}).get("text", ""),
            "metadata": match.get("metadata", {})
        })

    return retrieved
