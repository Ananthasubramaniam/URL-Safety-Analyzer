from analyzers.pattern_analyzer import PatternAnalyzer
from analyzers.network_analyzer import NetworkChecker
from analyzers.ml_analyser import ml_predict
from analyzers.blacklist_analyzer import check_blacklist
from utils.scoring_engine import ScoringEngine


class URLAnalyzer:
    

    def __init__(self):
        self.pattern_analyzer = PatternAnalyzer()
        self.network_checker = NetworkChecker()
        self.scoring_engine = ScoringEngine()

    def analyze(self, url: str) -> dict:

        # Run analyzers
        pattern_result = self.pattern_analyzer.analyze(url)
        network_result = self.network_checker.analyze(url)
        ml_result = ml_predict(url)
        blacklist_result = check_blacklist(url)

        # Extract raw scores safely
        pattern_score = pattern_result.get("score", 0)
        network_score = network_result.get("score", 0)
        ml_score = ml_result.get("ml_score", 0)
        blacklist_score = blacklist_result.get("score", 0)
        
        print("ML RESULT:", ml_result)
        print("BLACKLIST RESULT:", blacklist_result)


        # Calculate final weighted score
        final_score = self.scoring_engine.calculate_score(
            pattern_score=pattern_score,
            ml_score=ml_score,
            network_score=network_score,
            blacklist_score=blacklist_score
        )

        # Get verdict from scoring engine
        verdict = self.scoring_engine.get_verdict(final_score)

        # Optional explainability breakdown
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

        return {
            "score": final_score,
            "verdict": verdict,
            "details": details,
            "ml_probability": ml_result.get("ml_probability", None),
            "score_breakdown": breakdown
        }
