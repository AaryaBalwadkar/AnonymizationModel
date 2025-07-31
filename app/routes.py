from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import ALLOWED_FILE_TYPES, MAX_FILE_SIZE_MB, DEMO_LIMIT_ROWS
from fastapi.responses import FileResponse
from app.service.processor import process_file
from app.service.zip_util import zip_with_password

router = APIRouter()

@router.post("/anonymize")
async def anonymize_file(file: UploadFile = File(...), demo: bool = True):
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=413, detail="File too large.")

    try:
        limit = DEMO_LIMIT_ROWS if demo else None
        processed_path = process_file(contents, file.filename, limit_rows=limit)

        zip_path = zip_with_password(processed_path, password="secure123")

        return FileResponse(zip_path, media_type="application/zip", filename="anonymized.zip")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

