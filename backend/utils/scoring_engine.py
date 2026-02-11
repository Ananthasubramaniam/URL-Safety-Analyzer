class ScoringEngine:
    """
    Combines scores from different analyzers to produce a final verdict.
    """
    
    def calculate_score(self, pattern_score=0, ml_score=0, network_score=0, weights=None):
        if weights is None:
            # Default weights
            weights = {
                'pattern': 0.3,
                'ml': 0.4,
                'network': 0.3
            }
            
        final_score = (
            (pattern_score * weights['pattern']) +
            (ml_score * weights['ml']) +
            (network_score * weights['network'])
        )
        
        return round(final_score)

    def get_verdict(self, score: int) -> str:
        if score < 30:
            return "Safe"
        elif score < 70:
            return "Suspicious"
        else:
            return "Phishing / Unsafe"
