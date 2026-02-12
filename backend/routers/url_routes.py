from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.url_analyzer import URLAnalyzer

# NEW IMPORTS
from backend.database import SessionLocal
from backend.db_models.threat_log import ThreatLog

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

   
    db = SessionLocal()
    try:
        log = ThreatLog(
            url=request.url,
            verdict=result["verdict"],
            score=result["score"],
            ml_probability=result.get("ml_probability")
        )
        db.add(log)
        db.commit()
    finally:
        db.close()
  

    return UrlResponse(
        score=result["score"],
        verdict=result["verdict"],
        details=result["details"],
        ml_probability=result.get("ml_probability")
    )
