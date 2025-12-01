# app/main.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.agents.proposal_gen import create_proposal, generate_proposal_pdf_bytes

app = FastAPI(title="Insurance Proposal Generator")

# -----------------------------
# Request schema
# -----------------------------
class ProposalRequest(BaseModel):
    client_name: str
    age: int | None = None
    required_cover: str | None = None
    analysis: dict

# -----------------------------
# PROPOSAL GENERATOR ENDPOINT
# -----------------------------
@app.post("/proposal")
async def generate_proposal(request: ProposalRequest):
    try:
        client_profile = {
            "client_name": request.client_name,
            "age": request.age,
            "required_cover": request.required_cover
        }

        proposal_summary = await create_proposal(client_profile, request.analysis)

        best_option = request.analysis.get("best_option", {})

        pdf_bytes = generate_proposal_pdf_bytes(
            client_name=request.client_name,
            summary=proposal_summary,
            best_option=best_option
        )

        return StreamingResponse(
            pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={request.client_name}_proposal.pdf"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# ONBOARD ENDPOINT
# -----------------------------
@app.post("/onboard")
async def onboard_client(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("latin1", errors="ignore")

        extracted = {
            "client_name": "Unknown",
            "age": None,
            "required_cover": None,
            "raw_text": text
        }
        return extracted

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# FULL PROCESS ENDPOINT
# -----------------------------
@app.post("/full-process")
async def full_process(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("latin1", errors="ignore")

        extracted = {
            "client_name": "AutoClient",
            "age": 30,
            "required_cover": "5L",
            "raw_text": text
        }

        analysis = {
            "summary": "Auto analysis",
            "best_option": {
                "plan_name": "Plan A",
                "premium": "2000",
                "coverage": "5L"
            }
        }

        proposal = await create_proposal(extracted, analysis)

        pdf_bytes = generate_proposal_pdf_bytes(
            client_name=extracted["client_name"],
            summary=proposal,
            best_option=analysis["best_option"]
        )

        return StreamingResponse(
            pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=final_output.pdf"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
