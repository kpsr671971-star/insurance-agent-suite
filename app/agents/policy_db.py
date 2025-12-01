# app/agents/policy_db.py
import csv
from pathlib import Path

POLICY_FILE = Path(__file__).parents[1].joinpath("..", "data", "policies.csv").resolve()

def load_policies():
    policies = []
    # path may include 'app' so adjust
    p = Path(__file__).parents[2] / "data" / "policies.csv"
    with open(p, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                r['sum_insured'] = int(r['sum_insured'])
            except:
                r['sum_insured'] = 0
            policies.append(r)
    return policies

def find_relevant(policies, required_cover):
    return [p for p in policies if p['sum_insured'] >= required_cover] or sorted(policies, key=lambda x: x['sum_insured'], reverse=True)[:3]
