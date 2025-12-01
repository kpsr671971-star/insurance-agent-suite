# app/agents/ingest.py
from PyPDF2 import PdfReader
import io, re, json

def parse_client_pdf(raw_bytes: bytes) -> dict:
    """
    Minimal parser: extracts text and uses regex heuristics to find key fields.
    For demo, we fallback to sensible defaults.
    """
    try:
        reader = PdfReader(io.BytesIO(raw_bytes))
        text = ""
        for p in reader.pages:
            txt = p.extract_text() or ""
            text += txt + "\n"
    except Exception:
        text = raw_bytes.decode('utf-8', errors='ignore')

    # Heuristics: try to extract name, age, required_cover
    name = None
    age = None
    required_cover = None

    m = re.search(r"Name[:\-]\s*([A-Za-z\s]+)", text, re.IGNORECASE)
    if m:
        name = m.group(1).strip()
    m = re.search(r"Age[:\-]\s*(\d{1,2})", text, re.IGNORECASE)
    if m:
        age = int(m.group(1))
    m = re.search(r"Required Cover[:\-]\s*([\d,]+)", text, re.IGNORECASE)
    if m:
        required_cover = int(m.group(1).replace(",", ""))

    # Fallbacks for demo
    if not name:
        name = "Test Client"
    if not age:
        age = 35
    if not required_cover:
        required_cover = 500000

    return {"raw_text": text[:2000], "client_name": name, "age": age, "required_cover": required_cover}
