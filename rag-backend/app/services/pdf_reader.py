# app/services/pdf_reader.py
import fitz  # PyMuPDF

def read_pdf(file_content: bytes) -> str:
    """
    Extraire le texte du fichier PDF.
    
    Args:
        file_content (bytes): Le contenu du fichier PDF sous forme binaire.
    
    Returns:
        str: Le texte extrait du PDF.
    """
    doc = fitz.open(stream=file_content, filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text
