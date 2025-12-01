# app/agents/gap_analysis.py
def analyze_coverage(client_profile: dict, policies: list):
    required = client_profile.get('required_cover', 0)
    findings = []
    for p in policies:
        gap = max(0, required - p.get('sum_insured', 0))
        findings.append({
            "policy_id": p.get('id'),
            "policy_name": p.get('name'),
            "sum_insured": p.get('sum_insured'),
            "gap": gap,
            "suitable": p.get('sum_insured', 0) >= required
        })
    findings.sort(key=lambda x: x['gap'])
    summary = {
        "required_cover": required,
        "total_options": len(findings),
        "best_option": findings[0] if findings else None
    }
    return {"findings": findings, "summary": summary}
