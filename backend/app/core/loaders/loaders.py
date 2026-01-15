import os
import zipfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, Docx2txtLoader

# ----------------------------------------------------------
# Detect File Type and Use LangChain Loader
# ----------------------------------------------------------
def load_with_langchain(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return PyPDFLoader(file_path).load()

    elif ext == ".txt":
        return TextLoader(file_path, encoding="utf-8").load()

    elif ext == ".csv":
        return CSVLoader(file_path).load()
   
    elif ext == ".docx":
         return Docx2txtLoader(file_path).load()
    
    else:
        raise ValueError(f"Unsupported file format: {ext}")


# ----------------------------------------------------------
# ZIP Loader → Extract ZIP → Auto-load everything inside
# ----------------------------------------------------------
def load_zip_with_langchain(zip_path):
    extract_dir = "data/raw/zip_extracted"
    os.makedirs(extract_dir, exist_ok=True)

    # Extract files
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    docs = []
    for root, _, files in os.walk(extract_dir):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                docs.extend(load_with_langchain(full_path))
            except Exception:
                print(f"Skipping unsupported file: {file}")

    return docs


# ----------------------------------------------------------
# UNIVERSAL FILE LOADER
# ----------------------------------------------------------
def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".zip":
        return load_zip_with_langchain(file_path)
    
    return load_with_langchain(file_path)
