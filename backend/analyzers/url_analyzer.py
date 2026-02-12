from analyzers.pattern_analyzer import PatternAnalyzer
from analyzers.network_analyzer import NetworkChecker
from analyzers.ml_analyser import ml_predict
from analyzers.blacklist_analyzer import check_blacklist
from utils.scoring_engine import ScoringEngine
from utils.education_engine import EducationEngine


class URLAnalyzer:

    def __init__(self):
        self.pattern_analyzer = PatternAnalyzer()
        self.network_checker = NetworkChecker()
        self.scoring_engine = ScoringEngine()
        self.education_engine = EducationEngine()  

    def analyze(self, url: str) -> dict:

        
        pattern_result = self.pattern_analyzer.analyze(url)
        network_result = self.network_checker.analyze(url)
        ml_result = ml_predict(url)
        blacklist_result = check_blacklist(url)

       
        pattern_score = pattern_result.get("score", 0)
        network_score = network_result.get("score", 0)
        ml_score = ml_result.get("ml_score", 0)
        blacklist_score = blacklist_result.get("score", 0)

        
        final_score = self.scoring_engine.calculate_score(
            pattern_score=pattern_score,
            ml_score=ml_score,
            network_score=network_score,
            blacklist_score=blacklist_score
        )

      
        verdict = self.scoring_engine.get_verdict(final_score)

        
        breakdown = self.scoring_engine.breakdown(
            pattern_score,
            ml_score,
            network_score,
            blacklist_score
        )

        
        details = (
            pattern_result.get("details", []) +
            network_result.get("details", [])
        )

        if blacklist_result.get("details"):
            details.append(blacklist_result["details"])

        
        educational_tips = self.education_engine.generate_tips(
            details,
            final_score
        )

        return {
            "score": final_score,
            "verdict": verdict,
            "details": details,
            "ml_probability": ml_result.get("ml_probability", None),
            "score_breakdown": breakdown,
            "educational_tips": educational_tips   
        }
