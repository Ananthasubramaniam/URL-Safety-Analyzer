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
        
        # 2. IP Address check (Improved regex)
        # Matches IP addresses at the beginning or after protocol
        if item := re.search(r'^(?:https?:\/\/)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', url):
            score += 65 # High impact
            details.append(f"URL uses IP address ({item.group(1)}) instead of domain name.")
            
        # 3. Suspicious Extensions
        suspicious_exts = ['.exe', '.dmg', '.tar', '.zip', '.scr', '.bat', '.vbs']
        if any(url.endswith(ext) for ext in suspicious_exts):
            score += 50
            details.append("URL points to an executable or archive file.")
        
        # 4. @ Symbol (credential theft attempt)
        if '@' in url:
            score += 60 # High impact
            details.append("URL contains '@' symbol (likely credential harvesting).")
            
        # 5. Multiple subdomains
        if url.count('.') > 4:
            score += 20
            details.append("High number of subdomains detected.")
            
        # 6. Phishing Keywords Check
        phishing_keywords = [
            'login', 'signin', 'verify', 'update', 'account', 'security', 
            'banking', 'confirm', 'wallet', 'crypto', 'support', 'service'
        ]
        
        found_keywords = [kw for kw in phishing_keywords if kw in url.lower()]
        if found_keywords:
            score += 15 * len(found_keywords)
            details.append(f"Suspicious keywords detected: {', '.join(found_keywords)}")

        return {
            "score": min(score, 100),
            "details": details
        }
