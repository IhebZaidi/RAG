from io import BytesIO
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.pdf_reader import read_pdf
from app.services.docs_reader import read_docx

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Vérification du type de fichier
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        return JSONResponse(status_code=400, content={"error": "Only PDF and DOCX files are supported."})

    # Vérification de la taille du fichier
    if file.size > 5 * 1024 * 1024:  # Limite de 5 MB
        return JSONResponse(status_code=400, content={"error": "File size exceeds 5 MB."})

    try:
        content = await file.read()

        # Utiliser BytesIO pour simuler un objet fichier
        file_like_object = BytesIO(content)

        # Traitement en fonction du type de fichier
        if file.content_type == "application/pdf":
            text = read_pdf(file_like_object)  # Passer file_like_object au lieu de content
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = read_docx(file_like_object)  # Passer file_like_object au lieu de content

        return JSONResponse(content={"text": text})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
