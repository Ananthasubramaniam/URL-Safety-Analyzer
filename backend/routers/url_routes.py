from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.pattern_analyzer import PatternAnalyzer

router = APIRouter()

analyzer = PatternAnalyzer()


# Request schema
class UrlRequest(BaseModel):
    url: str


# Response schema
class UrlResponse(BaseModel):
    score: int
    verdict: str
    details: list[str]


@router.post("/analyze-url", response_model=UrlResponse)
def analyze_url(request: UrlRequest):

    result = analyzer.analyze(request.url)
    score = result["score"]

    if score < 25:
        verdict = "Low Risk"
    elif score < 60:
        verdict = "Medium Risk"
    else:
        verdict = "High Risk"

    return {
        "score": score,
        "verdict": verdict,
        "details": result["details"]
    }
