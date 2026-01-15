import uuid
import os
import sys
import traceback

# Add src directory to Python path for imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from app.core.preprocess.preprocess_and_chunk import preprocess_and_chunk_documents
from app.core.embeddings.embedder import embed_documents
from app.core.embeddings.clip_embedder import embed_image
from app.core.embeddings.ocr_reader import extract_text_from_image
from app.core.embeddings.blip_captioner import generate_caption
from app.core.vectorstore.vector_store import save_text_vectors, save_image_vectors


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def ingest_file_service(file_path: str):
    try:
        # Validate file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        session_id = str(uuid.uuid4())
        ext = os.path.splitext(file_path)[1].lower()
        
        print(f"[INFO] Processing file: {file_path}")
        print(f"[INFO] Session ID: {session_id}")
        print(f"[INFO] File extension: {ext}")

        # ---------------- IMAGE INGESTION ----------------
        if ext in IMAGE_EXTENSIONS:
            # 1️⃣ OCR
            ocr_text = extract_text_from_image(file_path).strip()

            # 2️⃣ Caption
            caption = generate_caption(file_path).strip()

            combined_text = f"""
IMAGE CAPTION:
{caption}

IMAGE OCR:
{ocr_text}
""".strip()

            # 3️⃣ Save OCR + caption as TEXT vectors
            if combined_text:
                text_embeddings = embed_documents([combined_text])
                save_text_vectors(
                    text_embeddings,
                    [{
                        "session_id": session_id,
                        "type": "image_text",
                        "modality": "image",
                        "source": file_path,
                        "text": combined_text
                    }],
                    [combined_text]
                )

            # 4️⃣ Save IMAGE vector (CLIP)
            image_embedding = embed_image(file_path)
            save_image_vectors(file_path, image_embedding, session_id)

            return {
                "status": "success",
                "session_id": session_id,
                "modality": "image"
            }

        # ---------------- DOCUMENT INGESTION ----------------
        else:
            print(f"[DEBUG] verify: Calling preprocess_and_chunk_documents for {file_path}")
            sys.stdout.flush()
            chunks, metadatas = preprocess_and_chunk_documents(file_path)
            print(f"[DEBUG] verify: Chunks created: {len(chunks)}")
            sys.stdout.flush()

            for i, meta in enumerate(metadatas):
                meta["session_id"] = session_id
                meta["type"] = "document"
                meta["modality"] = "text"
                meta["text"] = chunks[i]

            embeddings = embed_documents(chunks)
            save_text_vectors(embeddings, metadatas, chunks)

            return {
                "status": "success",
                "session_id": session_id,
                "modality": "document",
                "chunks": len(chunks)
            }
    
    except Exception as e:
        error_msg = f"Error processing file {file_path}: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise Exception(error_msg)
