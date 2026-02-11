from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.url_analyzer import URLAnalyzer

router = APIRouter()
analyzer = URLAnalyzer()


class UrlRequest(BaseModel):
    url: str


class UrlResponse(BaseModel):
    score: int
    verdict: str
    details: list[str]
    ml_probability: float | None = None


@router.post("/analyze-url", response_model=UrlResponse)
def analyze_url(request: UrlRequest):

    result = analyzer.analyze(request.url)

    return UrlResponse(
        score=result["score"],
        verdict=result["verdict"],
        details=result["details"],
        ml_probability=result.get("ml_probability")
    )
