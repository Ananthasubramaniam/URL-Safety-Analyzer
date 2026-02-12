from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from analyzers.url_analyzer import URLAnalyzer
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
    ml_probability: Optional[float] = None
    educational_tips: list[str] = []        # NEW
    score_breakdown: dict | None = None     # NEW


class HistoryItem(BaseModel):
    id: int
    url: str
    verdict: str
    score: int
    ml_probability: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True


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
        ml_probability=result.get("ml_probability"),
        educational_tips=result.get("educational_tips", []),   # NEW
        score_breakdown=result.get("score_breakdown")           # NEW
    )


@router.get("/history", response_model=List[HistoryItem])
def get_history():

    db = SessionLocal()
    try:
        logs = (
            db.query(ThreatLog)
            .order_by(ThreatLog.created_at.desc())
            .limit(50)
            .all()
        )
        return logs
    finally:
        db.close()
