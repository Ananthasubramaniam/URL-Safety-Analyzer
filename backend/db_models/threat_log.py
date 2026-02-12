from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class ThreatLog(Base):
    __tablename__ = "threat_logs"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    verdict = Column(String)
    score = Column(Integer)
    ml_probability = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
