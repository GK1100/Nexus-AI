import os
import uuid

from app.core.preprocess.preprocess_and_chunk import preprocess_and_chunk_documents
from app.core.embeddings.embedder import embed_documents
from app.core.embeddings.clip_embedder import embed_image
from app.core.vectorstore.vector_store import save_text_vectors, save_image_vectors
from app.core.retriever.retriever import retrieve_chunks
from app.core.retriever.image_retriever import retrieve_images
from app.core.generator.generator import generate_rag_answer
from app.core.embeddings.ocr_reader import extract_text_from_image
from app.core.embeddings.llava_reasoner import reason_about_image

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def detect_query_type(query: str) -> str:
    q = query.lower()
    if any(word in q for word in ["image", "figure", "diagram", "picture"]):
        return "image"
    return "text"


def main():
    session_id = str(uuid.uuid4())
    print(f"\n🧩 Session ID: {session_id}")

    print("\n📄 Enter file paths (min 1, max 3), comma separated:")
    paths = input("Files: ").strip().split(",")
    file_paths = [p.strip() for p in paths if p.strip()]

    if not (1 <= len(file_paths) <= 3):
        print("❌ Please provide between 1 and 3 files.")
        return

    # ---------------- INGEST FILES ----------------
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue

        # ---------- IMAGE ----------
        if file_path.lower().endswith(IMAGE_EXTENSIONS):
            print(f"\n🖼️ Processing image: {file_path}")

            # 1️⃣ OCR TEXT
            ocr_text = extract_text_from_image(file_path)

            if ocr_text.strip():
                embeddings = embed_documents([ocr_text])
                metadatas = [{
                    "session_id": session_id,
                    "type": "image",
                    "modality": "image",
                    "source": file_path,
                    "text": ocr_text
                }]
                save_text_vectors(embeddings, metadatas, [ocr_text])

            # 2️⃣ IMAGE EMBEDDING
            image_embedding = embed_image(file_path)
            save_image_vectors(file_path, image_embedding, session_id)

        # ---------- DOCUMENT ----------
        else:
            print(f"\n📄 Processing document: {file_path}")

            chunks, metadatas = preprocess_and_chunk_documents(file_path)

            for i, meta in enumerate(metadatas):
                meta["session_id"] = session_id
                meta["type"] = "document"
                meta["modality"] = "text"
                meta["text"] = chunks[i]

            embeddings = embed_documents(chunks)
            save_text_vectors(embeddings, metadatas, chunks)

    print("\n✅ All files ingested successfully.")

    # ---------------- QUERY LOOP ----------------
    while True:
        query = input("\n❓ Ask a question (type 'quit'): ").strip()
        if query.lower() == "quit":
            print("👋 Exiting RAG.")
            break

        query_type = detect_query_type(query)

        # Retrieve TEXT chunks (documents + OCR)
        retrieved_chunks = retrieve_chunks(
            query_text=query,
            top_k=8,
            filter={"session_id": session_id}
        )

        # Retrieve IMAGES only for image queries
        retrieved_images = []
        if query_type == "image":
            retrieved_images = retrieve_images(query, top_k=3)

            # LLaVA explanation
            image_explanations = []
            for img in retrieved_images:
                explanation = reason_about_image(
                    img["source"],
                    query
                )
                image_explanations.append(explanation)

            if image_explanations:
                retrieved_chunks.append({
                    "text": "\n".join(image_explanations),
                    "metadata": {"modality": "image"}
                })

        # FINAL ANSWER
        answer = generate_rag_answer(
            query,
            retrieved_chunks,
            retrieved_images
        )

        print("\n📌 FINAL ANSWER:")
        print(answer)


if __name__ == "__main__":
    main()
