from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from analyzers.url_analyzer import URLAnalyzer

# NEW IMPORTS
from database import SessionLocal
from db_models.threat_log import ThreatLog

router = APIRouter()
analyzer = URLAnalyzer()


class UrlRequest(BaseModel):
    url: str


class UrlResponse(BaseModel):
    score: int
    verdict: str
    breakdown: dict
    reasons: list[str]
    recommendations: list[str]
    ml_probability: Optional[float] = None


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
    try:
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
        except Exception as db_exc:
            print(f"Database logging failed: {db_exc}")
        finally:
            db.close()

        return UrlResponse(
            score=result["score"],
            verdict=result["verdict"],
            breakdown=result["breakdown"],
            reasons=result["reasons"],
            recommendations=result["recommendations"],
            ml_probability=result.get("ml_probability")
        )
    except Exception as e:
        # Graceful fallback to avoid returning stack trace
        return UrlResponse(
            score=0,
            verdict="Error",
            breakdown={"pattern": 0, "ml": 0, "network": 0},
            reasons=[f"An error occurred during analysis: {str(e)}"],
            recommendations=["Please try again later or contact support if the issue persists."],
            ml_probability=0
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


@router.delete("/history")
def clear_history():
    db = SessionLocal()
    try:
        db.query(ThreatLog).delete()
        db.commit()
        return {"message": "History cleared"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

from concurrent.futures import ThreadPoolExecutor

@router.post("/bulk-analyze")
def bulk_analyze(request: List[str]):
    results = []
    
    def analyze_single(url):
        try:
            return {
                "url": url,
                "result": analyzer.analyze(url)
            }
        except Exception as e:
            return {
                "url": url,
                "error": str(e)
            }

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(analyze_single, url) for url in request]
        for future in futures:
            results.append(future.result())
    
    return results
