class ScoringEngine:
    """
    Combines scores from different analyzers
    and produces final verdict.
    """

    def __init__(self, weights=None):
        self.weights = weights or {
            "pattern": 0.25,
            "ml": 0.25,
            "network": 0.25,
            "virustotal": 0.25,  
            "blacklist": 1.0      
        }

    def _normalize(self, score):
        return min(max(score, 0), 100)

    def calculate_score(
        self,
        pattern_score=0,
        ml_score=0,
        network_score=0,
        blacklist_score=0,
        virustotal_score=0  
    ):

        pattern_score = self._normalize(pattern_score)
        ml_score = self._normalize(ml_score)
        network_score = self._normalize(network_score)
        blacklist_score = self._normalize(blacklist_score)
        virustotal_score = self._normalize(virustotal_score)

        # 1. Blacklist Override
        if blacklist_score > 0:
            return max(blacklist_score, 95)

        # 2. Strong Single Indicators
        if pattern_score > 80 or ml_score > 80 or virustotal_score > 80:
            return max(pattern_score, ml_score, virustotal_score, 75)

        # 3. Weighted Score
        final_score = (
            (pattern_score * self.weights["pattern"]) +
            (ml_score * self.weights["ml"]) +
            (network_score * self.weights["network"]) +
            (virustotal_score * self.weights["virustotal"])  
        )

        return min(round(final_score), 100)

    def get_verdict(self, score: int) -> str:

        if score < 30:
            return "Safe"
        elif score < 65:
            return "Suspicious"
        else:
            return "Phishing / Unsafe"

    def breakdown(
        self,
        pattern_score,
        ml_score,
        network_score,
        blacklist_score=0,
        virustotal_score=0
    ):
        """
        Returns the raw scores from each analyzer layer for detailed reporting.
        """
        return {
            "pattern": round(pattern_score),
            "ml": round(ml_score),
            "network": round(network_score),
            "virustotal": round(virustotal_score),
            "blacklist": round(blacklist_score)
        }
 