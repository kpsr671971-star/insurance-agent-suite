import PyPDF2
from fastapi import UploadFile

def extract_client_details(file: UploadFile):
    try:
        pdf_reader = PyPDF2.PdfReader(file.file)

        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text() or ""

        if not full_text:
            return {
                "raw_text": "",
                "summary": "",
                "error": "No text extracted from PDF"
            }

        return {
            "raw_text": full_text,
            "summary": full_text[:200],
            "error": None
        }

    except Exception as e:
        return {
            "raw_text": "",
            "summary": "",
            "error": f"PDF processing failed: {str(e)}"
        }
