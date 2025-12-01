# app/full_process.py

import uuid
from fastapi import UploadFile

from app.pdf_reader import extract_client_details
from app.recommendation import recommend_policies
from app.agents.proposal_gen import generate_proposal_pdf


def run_full_process(client_file: UploadFile):

    # -----------------------------
    # 1 — Extract client details
    # -----------------------------
    details = extract_client_details(client_file)

    # -----------------------------
    # 2 — Generate recommendation
    # -----------------------------
    recommendation = recommend_policies(details)

    # -----------------------------
    # 3 — Generate proposal PDF
    # -----------------------------
    pdf_name = f"proposal_{uuid.uuid4().hex}.pdf"

    generate_proposal_pdf(
        pdf_name,
        client_name=details.get("client_name", "Client"),
        summary=recommendation.get("summary", "No summary generated"),
        best_option=recommendation.get("best_option", {})
    )

    # -----------------------------
    # 4 — Final output
    # -----------------------------
    return {
        "details": details,
        "recommendation": recommendation,
        "proposal_pdf": pdf_name
    }
