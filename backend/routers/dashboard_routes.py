from fastapi import APIRouter
from sqlalchemy import func
from database import SessionLocal
from db_models.threat_log import ThreatLog

router = APIRouter()

# ---------- SUMMARY ----------
@router.get("/dashboard/summary")
def get_summary():
    db = SessionLocal()
    try:
        total = db.query(ThreatLog).count()

        safe = db.query(ThreatLog).filter(ThreatLog.verdict == "Safe").count()
        suspicious = db.query(ThreatLog).filter(ThreatLog.verdict == "Suspicious").count()
        phishing = db.query(ThreatLog).filter(ThreatLog.verdict == "Phishing / Unsafe").count()

        return {
            "total_scans": total,
            "safe": safe,
            "suspicious": suspicious,
            "phishing": phishing
        }
    finally:
        db.close()


# ---------- VERDICT DISTRIBUTION ----------
@router.get("/dashboard/distribution")
def verdict_distribution():
    db = SessionLocal()
    try:
        results = (
            db.query(ThreatLog.verdict, func.count(ThreatLog.id))
            .group_by(ThreatLog.verdict)
            .all()
        )

        return {verdict: count for verdict, count in results}
    finally:
        db.close()


# ---------- RECENT THREATS ----------
@router.get("/dashboard/recent")
def recent_threats():
    db = SessionLocal()
    try:
        logs = (
            db.query(ThreatLog)
            .filter(ThreatLog.verdict != "Safe")
            .order_by(ThreatLog.created_at.desc())
            .limit(10)
            .all()
        )

        return [
            {
                "url": log.url,
                "verdict": log.verdict,
                "score": log.score,
                "ml_probability": log.ml_probability,
                "time": log.created_at
            }
            for log in logs
        ]
    finally:
        db.close()
