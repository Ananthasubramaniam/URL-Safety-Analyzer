from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Request schema
class UrlRequest(BaseModel):
    url: str


# Response schema
class UrlResponse(BaseModel):
    score: int
    verdict: str
    message: str


@router.post("/analyze-url", response_model=UrlResponse)
def analyze_url(request: UrlRequest):

    # MOCK LOGIC — real logic later
    score = 45

    if score < 30:
        verdict = "Low Risk"
    elif score < 70:
        verdict = "Medium Risk"
    else:
        verdict = "High Risk"

    return {
        "score": score,
        "verdict": verdict,
        "message": f"Analysis completed for {request.url}"
    }
    