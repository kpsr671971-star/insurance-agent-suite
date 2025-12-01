# app/agents/proposal_gen.py
from app.llm_client import generate_text
from fpdf import FPDF
import io

# -----------------------------
# Generate proposal text (async)
# -----------------------------
async def create_proposal(client_profile: dict, analysis: dict):
    """
    Generates professional insurance proposal text using LLM.
    """
    prompt = f"""
    Create a professional insurance proposal for {client_profile.get('client_name')}.
    Client age: {client_profile.get('age', 'N/A')}.
    Required cover: {client_profile.get('required_cover', 'N/A')}.
    Analysis summary: {analysis.get('summary', '')}
    Provide: executive summary, recommended policy, coverage table, next steps (max 350 words).
    Return as plain text.
    """
    resp = await generate_text(prompt)
    return {"proposal_text": resp['text'], "prompt": prompt}

# -----------------------------
# Generate PDF and save to file (optional)
# -----------------------------
def generate_proposal_pdf(pdf_path: str, client_name: str, summary: dict, best_option: dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, txt="Insurance Proposal Report", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Client Name: {client_name}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Best Option Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(2)
    for key, value in best_option.items():
        pdf.multi_cell(0, 8, txt=f"{key}: {value}")

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Proposal Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(2)
    pdf.multi_cell(0, 8, txt=summary.get("proposal_text", ""))

    pdf.output(pdf_path)

# -----------------------------
# Generate PDF as bytes (FastAPI-friendly)
# -----------------------------
def generate_proposal_pdf_bytes(client_name: str, summary: dict, best_option: dict) -> io.BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, txt="Insurance Proposal Report", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Client Name: {client_name}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Best Option Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(2)
    for key, value in best_option.items():
        pdf.multi_cell(0, 8, txt=f"{key}: {value}")

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Proposal Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(2)
    pdf.multi_cell(0, 8, txt=summary.get("proposal_text", ""))

    # Convert PDF to bytes for StreamingResponse
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return io.BytesIO(pdf_bytes)
