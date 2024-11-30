from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.pdf_reader import read_pdf
from app.services.docs_reader import read_docx  # Importation du lecteur DOCX
from app.services.qa_service import get_answer
import logging
from io import BytesIO

router = APIRouter()

@router.post("/ask-question/")
async def ask_question(file: UploadFile = File(...), question: str = ""):
    """
    Endpoint pour poser une question basée sur le contenu d'un CV téléchargé (PDF ou DOCX).
    """
    logging.info(f"Received question: {question}")
    
    if not question.strip():
        raise HTTPException(status_code=400, detail="The 'question' parameter is required.")

    try:
        # Lire le contenu du fichier
        file_content = await file.read()
        logging.info(f"File size: {len(file_content)} bytes")
        
        # Créer un objet BytesIO à partir du contenu binaire pour simuler un fichier
        file_like_object = BytesIO(file_content)

        # Vérifier le type de fichier (PDF ou DOCX)
        if file.content_type == "application/pdf":
            # Extraire le texte du fichier PDF
            cv_text = read_pdf(file_like_object)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Extraire le texte du fichier DOCX
            cv_text = read_docx(file_like_object)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or DOCX file.")

        if not cv_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the uploaded file.")

        # Obtenir une réponse à la question
        answer = get_answer(question, cv_text)
        return {"answer": answer}

    except ValueError as ve:
        logging.error(f"Value error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the file.")
