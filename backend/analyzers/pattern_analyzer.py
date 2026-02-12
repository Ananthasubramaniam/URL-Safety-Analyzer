import re
import math
from collections import Counter
from urllib.parse import urlparse


class PatternAnalyzer:

    def shannon_entropy(self, text):
        counts = Counter(text)
        probs = [c / len(text) for c in counts.values()]
        return -sum(p * math.log2(p) for p in probs)

    def analyze(self, url: str) -> dict:
        score = 0
        details = []

        parsed = urlparse(url)
        domain = parsed.hostname or url

        # Length
        if len(url) > 75:
            score += 20
            details.append("URL is unusually long.")

        # HTTPS check
        if not url.startswith("https://"):
            score += 10
            details.append("URL does not use HTTPS.")

        # IP address
        if re.search(r'^(?:https?:\/\/)?\d{1,3}(\.\d{1,3}){3}', url):
            score += 60
            details.append("URL uses IP address instead of domain.")

        # Hyphen abuse
        if domain.count('-') > 3:
            score += 15
            details.append("Excessive hyphens in domain.")

        # Digit density
        digits = sum(c.isdigit() for c in url)
        if digits / max(len(url), 1) > 0.3:
            score += 15
            details.append("High digit density in URL.")

        # Encoded characters
        if "%" in url:
            score += 10
            details.append("Encoded characters detected.")

        # Homograph detection (basic)
        if "xn--" in domain:
            score += 40
            details.append("Possible homograph attack (punycode detected).")

        # Phishing keywords
        phishing_keywords = [
            "login", "signin", "verify", "update",
            "account", "security", "confirm",
            "wallet", "crypto", "support"
        ]

        found = [kw for kw in phishing_keywords if kw in url.lower()]
        if found:
            score += 15 * len(found)
            details.append(f"Suspicious keywords: {', '.join(found)}")

        # Entropy complexity
        entropy = self.shannon_entropy(domain)
        if entropy > 4.2:
            score += 20
            details.append("High entropy domain (random-looking).")

        return {
            "score": min(score, 100),
            "details": details
        }
