from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.email_analyzer import EmailAnalyzer

router = APIRouter()
analyzer = EmailAnalyzer()


# -------- REQUEST MODEL --------
class EmailRequest(BaseModel):
    subject: str
    body: str


# -------- RESPONSE MODEL --------
class EmailResponse(BaseModel):
    score: int
    verdict: str
    details: list[str]
    ml_probability: float | None = None


# -------- ROUTE --------
@router.post("/analyze-email", response_model=EmailResponse)
def analyze_email(request: EmailRequest):

    result = analyzer.analyze(
        subject=request.subject,
        body=request.body
    )

    return EmailResponse(
        score=result["score"],
        verdict=result["verdict"],
        details=result["details"],
        ml_probability=result.get("ml_probability")
    )
