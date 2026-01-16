from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import os
import shutil

from app.services.ingest_service import ingest_file_service

router = APIRouter()

# Use absolute path for upload directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

print(f"[INFO] Upload directory: {UPLOAD_DIR}")


@router.post("/file")
async def ingest_file(file: UploadFile = File(...)):
    try:
        print(f"[INFO] Received file upload: {file.filename}")
        print(f"[INFO] Content type: {file.content_type}")
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        print(f"[INFO] Saving to: {file_path}")

        # Async file write
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print(f"[INFO] File saved successfully")
        print(f"[INFO] Starting ingestion process...")

        result = ingest_file_service(file_path)
        
        print(f"[INFO] Ingestion completed successfully")
        return result

    except Exception as e:
        print(f"[ERROR] Upload failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )
