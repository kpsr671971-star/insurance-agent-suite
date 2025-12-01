from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RecommendationRequest(BaseModel):
    client_name: str
    goal: str

@router.post("/recommend")
def recommend(req: RecommendationRequest):
    # Dummy logic — replace with real engine later
    if req.goal.lower() == "retirement":
        return {
            "recommended_policy": "Retirement Annuity P010",
            "reason": "Best long-term guaranteed return option",
            "next_steps": [
                "Review benefits with client",
                "Check premium affordability",
                "Prepare proposal PDF"
            ]
        }

    return {
        "recommended_policy": "Family Life Protect P001",
        "reason": "Most balanced option for common life planning needs",
        "next_steps": ["Collect KYC", "Prepare quote", "Schedule pitch call"]
    }
def recommend_policies(user_input):
    # Dummy recommendation logic for now
    return {
        "policy": "Basic Life Insurance",
        "premium": 12000,
        "reason": "Based on age, income, and goals."
    }
    
