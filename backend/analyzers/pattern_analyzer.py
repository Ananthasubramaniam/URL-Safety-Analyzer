import re

class PatternAnalyzer:
    """
    Analyzes URL based on static patterns and rules.
    """
    
    def analyze(self, url: str) -> dict:
        score = 0
        details = []
        
        # 1. Length Check
        if len(url) > 75:
            score += 20
            details.append("URL is suspiciously long (possible obfuscation).")
        
        # 2. IP Address check
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
            score += 30
            details.append("URL uses IP address instead of domain name.")
            
        # 3. Suspicious Extensions
        suspicious_exts = ['.exe', '.dmg', '.tar', '.zip', '.scr']
        if any(url.endswith(ext) for ext in suspicious_exts):
            score += 40
            details.append("URL points to an executable or archive file.")
        
        # 4. @ Symbol (credential theft attempt)
        if '@' in url:
            score += 50
            details.append("URL contains '@' symbol (possible credential harvesting).")
            
        # 5. Multiple subdomains
        if url.count('.') > 4:
            score += 15
            details.append("High number of subdomains detected.")

        return {
            "score": min(score, 100),
            "details": details
        }
