# app/orchestrator.py
from app.agents.ingest import parse_client_pdf
from app.agents.policy_db import load_policies, find_relevant
from app.agents.gap_analysis import analyze_coverage
from app.agents.proposal_gen import create_proposal

async def start_onboarding(raw_bytes: bytes):
    # 1. Ingest
    client = parse_client_pdf(raw_bytes)
    # 2. Load policies & find relevant
    policies = load_policies()
    relevant = find_relevant(policies, client.get('required_cover', 0))
    # 3. Gap analysis
    analysis = analyze_coverage(client, relevant)
    # 4. Proposal generation (LLM)
    proposal = await create_proposal(client, analysis)
    # 5. Return combined result
    return {"client": client, "analysis": analysis, "proposal": proposal}
