class ScoringEngine:
    """
    Combines scores from different analyzers
    and produces final verdict.
    """

    def __init__(self, weights=None):
        self.weights = weights or {
            "pattern": 0.3, # Increased from 0.1
            "ml": 0.3,      # Increased from 0.2
            "network": 0.4, # Increased from 0.1
            "blacklist": 1.0 # Immediate override
        }

    def _normalize(self, score):
        return min(max(score, 0), 100)

    def calculate_score(self, pattern_score=0, ml_score=0, network_score=0, blacklist_score=0):

        pattern_score = self._normalize(pattern_score)
        ml_score = self._normalize(ml_score)
        network_score = self._normalize(network_score)
        blacklist_score = self._normalize(blacklist_score)
        
        # 1. Blacklist Check: Immediate Phishing Verdict
        if blacklist_score > 0:
            return max(blacklist_score, 95)

        # 2. Key Indicator Check: If any single component is very high, force Suspicious/Unsafe
        # This prevents a "Safe" network check from masking a "Malicious" pattern
        if pattern_score > 80 or ml_score > 80:
             return max(pattern_score, ml_score, 75) # Minimum Suspicious/Unsafe

        final_score = (
            (pattern_score * self.weights["pattern"]) +
            (ml_score * self.weights["ml"]) +
            (network_score * self.weights["network"])
        )

        # Ensure we don't exceed 100
        return min(round(final_score), 100)

    def get_verdict(self, score: int) -> str:

        if score < 30:
            return "Safe"
        elif score < 65: # Tightened threshold
            return "Suspicious"
        else:
            return "Phishing / Unsafe"

    def breakdown(self, pattern_score, ml_score, network_score, blacklist_score=0):
        return {
            "pattern_contribution": round(pattern_score * self.weights["pattern"]),
            "ml_contribution": round(ml_score * self.weights["ml"]),
            "network_contribution": round(network_score * self.weights["network"]),
            "blacklist_contribution": blacklist_score # Direct impact
        }
