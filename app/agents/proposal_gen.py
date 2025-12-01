# app/agents/proposal_gen.py

from fpdf import FPDF
import io

# -----------------------------------------
# Generate PDF in memory (final version)
# -----------------------------------------
def generate_proposal_pdf_bytes(client_name: str, summary: dict, best_option: dict) -> io.BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Insurance Proposal Report", ln=True, align="C")

    # Client Name
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Client Name: {client_name}", ln=True)

    # Best Option Section
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Best Option Details:", ln=True)

    pdf.set_font("Arial", "", 12)
    for key, value in best_option.items():
        pdf.multi_cell(0, 8, txt=f"{key}: {value}")

    # Summary Section
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Proposal Summary:", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, txt=summary.get("proposal_text", ""))

    # Return PDF as bytes
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return io.BytesIO(pdf_bytes)
