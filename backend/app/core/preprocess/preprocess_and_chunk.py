# import re
# from transformers import AutoTokenizer
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from _1loaders.loaders import load_file

# def clean_text(text: str) -> str:
#     if not isinstance(text, str):
#         return ""
#     text = text.replace("\n", " ")
#     text = re.sub(r"\s+", " ", text)
#     return text.strip()

# def extract_title_from_docs(docs):
#     first_page = docs[0].page_content
#     lines = first_page.split("\n")
#     title = lines[0].strip()
#     return title

# def preprocess_and_chunk_documents(file_path):
#     docs = load_file(file_path)

#     # ---- Page 1 (title + abstract) ----
#     page1 = clean_text(docs[0].page_content)

#     # ---- Rest of document ----
#     rest = clean_text(" ".join([d.page_content for d in docs[1:]]))

#     tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-en")

#     splitter_small = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
#         tokenizer=tokenizer,
#         chunk_size=200,
#         chunk_overlap=20
#     )

#     splitter_large = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
#         tokenizer=tokenizer,
#         chunk_size=480,
#         chunk_overlap=60
#     )

#     page1_docs = splitter_small.create_documents([page1])
#     rest_docs = splitter_large.create_documents([rest])

#     all_docs = page1_docs + rest_docs

#     chunks = [doc.page_content for doc in all_docs]
#     metadatas = [
#         {"source": file_path, "chunk_id": i}
#         for i in range(len(chunks))
#     ]

#     return chunks, metadatas

import re
import uuid
from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.loaders.loaders import load_file


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_and_chunk_documents(file_path):
    # 🔹 Create session id (CRITICAL)
    session_id = str(uuid.uuid4())

    docs = load_file(file_path)

    # ---- Page 1 ----
    page1 = clean_text(docs[0].page_content)

    # ---- Remaining pages ----
    rest = clean_text(" ".join([d.page_content for d in docs[1:]]))

    tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-en")

    splitter_small = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer=tokenizer,
        chunk_size=200,
        chunk_overlap=20
    )

    splitter_large = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer=tokenizer,
        chunk_size=480,
        chunk_overlap=60
    )

    page1_docs = splitter_small.create_documents([page1])
    rest_docs = splitter_large.create_documents([rest])

    all_docs = page1_docs + rest_docs

    chunks = [doc.page_content for doc in all_docs]

    # 🔹 FIXED METADATA
    metadatas = [
        {
            "source": file_path,
            "chunk_id": i,
            "session_id": session_id,
            "modality": "text"
        }
        for i in range(len(chunks))
    ]

    return chunks, metadatas
