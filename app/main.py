# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.agents.proposal_gen import generate_proposal_pdf_bytes

app = FastAPI(title="Insurance Proposal Generator – Final Version")

# -----------------------------------------
# Request Schema
# -----------------------------------------
class ProposalRequest(BaseModel):
    client_name: str
    age: int | None = None
    required_cover: str | None = None
    summary: str                    # <- YOU control this text
    best_option: dict               # <- plan_name, premium, coverage


# -----------------------------------------
# Generate Proposal PDF (final submission safe)
# -----------------------------------------
@app.post("/proposal")
async def generate_proposal(request: ProposalRequest):
    try:
        pdf_bytes = generate_proposal_pdf_bytes(
            client_name=request.client_name,
            summary={"proposal_text": request.summary},
            best_option=request.best_option
        )

        return StreamingResponse(
            pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                f"attachment; filename={request.client_name}_proposal.pdf"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------
# PDF from file upload (optional)
# -----------------------------------------
@app.post("/full-process")
async def full_process(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("latin1", errors="ignore")

        analysis = {
            "summary": text[:500],
            "best_option": {
                "plan_name": "Auto Plan",
                "premium": "2000",
                "coverage": "5L"
            }
        }

        pdf_bytes = generate_proposal_pdf_bytes(
            client_name="AutoClient",
            summary={"proposal_text": analysis["summary"]},
            best_option=analysis["best_option"]
        )

        return StreamingResponse(
            pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=auto.pdf"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
