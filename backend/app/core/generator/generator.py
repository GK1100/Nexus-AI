import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_rag_answer(query, retrieved_chunks, retrieved_images):
    text_context = ""
    image_context = ""

    for item in retrieved_chunks:
        meta = item.get("metadata", {})
        if meta.get("modality") == "image":
            image_context += item.get("text", "") + "\n\n"
        else:
            text_context += item.get("text", "") + "\n\n"

    # If absolutely no usable context
    if not text_context.strip() and not image_context.strip():
        return "The provided context does not contain enough information to answer this question."

    prompt = f"""
You are a Retrieval-Augmented Generation (RAG) assistant.

Answer the QUESTION using ONLY the information provided in the CONTEXT.
Do not assume or invent information.

QUESTION:
{query}

CONTEXT:
{text_context}
{image_context}

FINAL ANSWER:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
