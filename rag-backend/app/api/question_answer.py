from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.pdf_reader import read_pdf
from app.services.qa_service import get_answer
import logging

router = APIRouter()

@router.post("/ask-question/")
async def ask_question(file: UploadFile = File(...), question: str = ""):
    """
    Endpoint pour poser une question basée sur le contenu d'un CV téléchargé.
    """
    logging.info(f"Received question: {question}")
    
    if not question.strip():
        raise HTTPException(status_code=400, detail="The 'question' parameter is required.")

    try:
        # Lire le contenu du fichier PDF
        file_content = await file.read()
        logging.info(f"File size: {len(file_content)} bytes")

        # Extraire le texte du CV
        cv_text = read_pdf(file_content)

        if not cv_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the uploaded CV.")

        # Obtenir une réponse à la question
        answer = get_answer(question, cv_text)
        return {"answer": answer}

    except ValueError as ve:
        logging.error(f"Value error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the file.")
