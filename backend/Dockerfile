FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ THIS LINE FIXES YOUR ERROR
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install -r requirements.txt

# PRELOAD EMBEDDING MODEL (ADD HERE)
RUN python - <<EOF
from langchain_huggingface import HuggingFaceEmbeddings
HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("✅ Embedding model preloaded at build time")
EOF

COPY . .

EXPOSE 8000

# Add timeout configurations to handle long-running operations
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
    "--timeout-keep-alive", "75", \
    "--timeout-graceful-shutdown", "30"]