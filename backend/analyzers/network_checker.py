import socket
import ssl
import whois
from datetime import datetime

class NetworkChecker:
    """
    Performs live network checks (WHOIS, SSL, DNS).
    """

    def check_domain_age(self, domain: str) -> dict:
        try:
            w = whois.whois(domain)
            creation_date = w.creation_date
            
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
                
            if not creation_date:
                return {"score": 10, "details": "Could not determine domain age."}
            
            age_days = (datetime.now() - creation_date).days
            
            if age_days < 30:
                return {"score": 50, "detail": f"Domain is very new ({age_days} days old)."}
            elif age_days < 180:
                return {"score": 20, "detail": f"Domain is relatively new ({age_days} days old)."}
            
            return {"score": 0, "detail": "Domain age is valid."}
            
        except Exception as e:
            return {"score": 0, "detail": f"WHOIS lookup failed or private: {str(e)}"}

    def check_ssl(self, domain: str) -> dict:
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(3.0)
                s.connect((domain, 443))
                cert = s.getpeercert()
                return {"score": 0, "detail": "Valid SSL certificate found."}
        except Exception:
            return {"score": 30, "detail": "No valid SSL certificate found."}
            
    def analyze(self, url: str) -> dict:
        from urllib.parse import urlparse
        try:
            domain = urlparse(url).netloc
            if not domain:
                domain = url.split('/')[0] # fallback
                
            age_result = self.check_domain_age(domain)
            ssl_result = self.check_ssl(domain)
            
            total_score = age_result['score'] + ssl_result['score']
            details = []
            if age_result.get('detail'): details.append(age_result['detail'])
            if ssl_result.get('detail'): details.append(ssl_result['detail'])
            
            return {
                "score": min(total_score, 100),
                "details": details
            }
        except Exception as e:
             return {
                "score": 0,
                "details": [f"Network check error: {str(e)}"]
            }
