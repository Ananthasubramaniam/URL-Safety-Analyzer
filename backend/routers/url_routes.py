from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.pattern_analyzer import PatternAnalyzer
from analyzers.network_checker import NetworkChecker
from utils.scoring_engine import ScoringEngine
from utils.helpers import is_valid_url

router = APIRouter()

# Initialize tools
pattern_analyzer = PatternAnalyzer()
network_checker = NetworkChecker()
scoring_engine = ScoringEngine()

# Request schema
class UrlRequest(BaseModel):
    url: str

# Response schema
class UrlResponse(BaseModel):
    score: int
    verdict: str
    message: str
    details: dict

@router.post("/analyze-url", response_model=UrlResponse)
def analyze_url(request: UrlRequest):
    url = request.url
    
    if not is_valid_url(url):
         return {
            "score": 0,
            "verdict": "Error",
            "message": "Invalid URL format provided.",
            "details": {}
        }

    # 1. Pattern Analysis
    pattern_result = pattern_analyzer.analyze(url)
    
    # 2. Network Analysis
    network_result = network_checker.analyze(url)
    
    # 3. ML Analysis (Placeholder for now)
    ml_result = {"score": 0, "details": "ML model not loaded yet."} # TODO: Add ML analyzer

    # 4. Calculate Final Score
    final_score = scoring_engine.calculate_score(
        pattern_score=pattern_result['score'],
        network_score=network_result['score'],
        ml_score=ml_result['score']
    )
    
    # 5. Get Verdict
    verdict = scoring_engine.get_verdict(final_score)
    
    # Aggregate details
    all_details = {
        "pattern_analysis": pattern_result['details'],
        "network_analysis": network_result['details'],
        "ml_analysis": ml_result['details']
    }

    return {
        "score": final_score,
        "verdict": verdict,
        "message": f"Analysis completed for {url}",
        "details": all_details
    }
    