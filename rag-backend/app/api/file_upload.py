from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.pdf_reader import read_pdf

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported."})

    if file.size > 5 * 1024 * 1024:  # Limite de 5 MB
        return JSONResponse(status_code=400, content={"error": "File size exceeds 5 MB."})

    try:
        content = await file.read()
        text = read_pdf(content)
        return JSONResponse(content={"text": text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
