from app.core.retriever.retriever import retrieve_chunks
from app.core.retriever.image_retriever import retrieve_images
from app.core.generator.generator import generate_rag_answer


def query_service(question: str, session_id: str):
    retrieved_chunks = retrieve_chunks(
        question,
        filter={"session_id": session_id}
    )

    retrieved_images = retrieve_images(question)

    return generate_rag_answer(
        query=question,
        retrieved_chunks=retrieved_chunks,
        retrieved_images=retrieved_images
    )
