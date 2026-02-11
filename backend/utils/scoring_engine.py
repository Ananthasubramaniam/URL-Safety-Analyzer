class ScoringEngine:
       def __init__(self, weights=None):
        
        self.weights = weights or {
            "pattern": 0.3,
            "ml": 0.4,
            "network": 0.3
        }

        def _normalize(self, score):
            
            return min(max(score, 0), 100)

        def calculate_score(self, pattern_score=0, ml_score=0, network_score=0):
            

            # Defensive normalization
            pattern_score = self._normalize(pattern_score)
            ml_score = self._normalize(ml_score)
            network_score = self._normalize(network_score)

            final_score = (
                (pattern_score * self.weights["pattern"]) +
                (ml_score * self.weights["ml"]) +
                (network_score * self.weights["network"])
            )

            return round(final_score)

        def get_verdict(self, score: int) -> str:
            

            if score < 30:
                return "Safe"
            elif score < 70:
                return "Suspicious"
            else:
                return "Phishing / Unsafe"

        def breakdown(self, pattern_score, ml_score, network_score):
            

            return {
                "pattern_contribution": round(pattern_score * self.weights["pattern"]),
                "ml_contribution": round(ml_score * self.weights["ml"]),
                "network_contribution": round(network_score * self.weights["network"]),
            }
