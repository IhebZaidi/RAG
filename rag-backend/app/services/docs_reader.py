# app/services/docs_reader.py
from docx import Document

def read_docx(file_content: bytes) -> str:
    """
    Extraire le texte d'un fichier DOCX.
    
    Args:
        file_content (bytes): Le contenu du fichier DOCX sous forme binaire.
    
    Returns:
        str: Le texte extrait du fichier DOCX.
    """
    document = Document(file_content)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    return text
