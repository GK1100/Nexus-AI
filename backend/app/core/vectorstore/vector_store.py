import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

from app.core.embeddings.embedder import embed_documents
from app.core.embeddings.ocr_reader import extract_text_from_image
from app.core.embeddings.blip_captioner import generate_caption

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

TEXT_INDEX_NAME = "multimodal-documents"
IMAGE_INDEX_NAME = "multimodal-image"

pc = Pinecone(api_key=PINECONE_API_KEY)


# -------------------------------------------------
# INDEX INITIALIZATION
# -------------------------------------------------
def init_index(name, dimension):
    existing = [i["name"] for i in pc.list_indexes()]

    if name not in existing:
        pc.create_index(
            name=name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_ENV
            )
        )

    return pc.Index(name)


# -------------------------------------------------
# TEXT VECTOR STORAGE
# -------------------------------------------------
def save_text_vectors(embeddings, metadatas, chunks):
    if not embeddings:
        return

    index = init_index(TEXT_INDEX_NAME, len(embeddings[0]))

    # Batch upsert for better performance
    vectors = []
    for i, emb in enumerate(embeddings):
        vectors.append({
            "id": f"text_{metadatas[i]['session_id']}_{i}",
            "values": emb,
            "metadata": {
                "text": chunks[i][:1000],  # Limit metadata size to 1000 chars
                **metadatas[i]
            }
        })

    # Upsert in batches of 100 (Pinecone limit)
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(batch)
        print(f"[INFO] Upserted batch {i//batch_size + 1}/{(len(vectors)-1)//batch_size + 1}")


# -------------------------------------------------
# IMAGE VECTOR STORAGE (CLIP + OCR + BLIP)
# -------------------------------------------------
def save_image_vectors(image_path, embedding, session_id):
    # ---------- CLIP IMAGE VECTOR ----------
    image_index = init_index(IMAGE_INDEX_NAME, len(embedding))

    image_index.upsert([{
        "id": f"img_{session_id}_{os.path.basename(image_path)}",
        "values": embedding,
        "metadata": {
            "source": image_path,
            "type": "image",
            "modality": "image",
            "session_id": session_id
        }
    }])

    # ---------- OCR + BLIP → TEXT ----------
    ocr_text = extract_text_from_image(image_path).strip()
    caption = generate_caption(image_path).strip()

    # ❌ Do NOT store weak or empty image context
    if not ocr_text and not caption:
        return

    combined_text = f"""
IMAGE CAPTION:
{caption}

IMAGE OCR:
{ocr_text}
""".strip()

    text_embeddings = embed_documents([combined_text])

    save_text_vectors(
        text_embeddings,
        [{
            "source": image_path,
            "type": "image_text",
            "modality": "image",
            "session_id": session_id
        }],
        [combined_text]
    )
