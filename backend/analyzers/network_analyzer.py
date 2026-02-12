import socket
import ssl
import whois
import requests
from datetime import datetime
from urllib.parse import urlparse


class NetworkChecker:
    def extract_domain(self, url: str) -> str:
        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        return parsed.hostname or url

    def check_dns(self, domain: str) -> dict:
        try:
            ip = socket.gethostbyname(domain)
            return {"score": 0, "detail": f"Domain resolves to IP {ip}.", "ip": ip}
        except Exception:
            return {"score": 40, "detail": "DNS resolution failed.", "ip": None}

    def check_domain_age(self, domain: str) -> dict:
        try:
            w = whois.whois(domain)
            creation_date = w.creation_date

            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if not creation_date:
                return {"score": 15, "detail": "Domain age unknown."}

            age_days = (datetime.now() - creation_date).days

            if age_days < 30:
                return {"score": 50, "detail": f"Very new domain ({age_days} days old)."}
            elif age_days < 180:
                return {"score": 25, "detail": f"Recently registered domain ({age_days} days old)."}

            return {"score": 0, "detail": "Domain age acceptable."}

        except Exception:
            return {"score": 20, "detail": "WHOIS lookup failed or hidden."}

    def check_ssl(self, domain: str) -> dict:
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(3.0) # Tightened timeout
                s.connect((domain, 443))
                cert = s.getpeercert()

                expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                if expiry < datetime.utcnow():
                    return {"score": 40, "detail": "SSL certificate expired."}

                return {"score": 0, "detail": "Valid SSL certificate."}

        except Exception:
            return {"score": 35, "detail": "SSL missing or invalid."}

    def check_geolocation(self, ip: str) -> dict:
        if not ip:
            return {"detail": "IP geolocation unavailable."}

        try:
            # Use a faster timeout for geolocation
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
            data = response.json()
            country = data.get("country", "Unknown")
            return {"detail": f"IP located in {country}."}
        except Exception:
            return {"detail": "IP geolocation lookup failed."}

    def analyze(self, url: str) -> dict:
        try:
            domain = self.extract_domain(url)

            dns_result = self.check_dns(domain)
            age_result = self.check_domain_age(domain)
            ssl_result = self.check_ssl(domain)
            geo_result = self.check_geolocation(dns_result.get("ip"))

            total_score = (
                dns_result["score"] +
                age_result["score"] +
                ssl_result["score"]
            )

            details = [
                dns_result["detail"],
                age_result["detail"],
                ssl_result["detail"],
                geo_result["detail"]
            ]

            return {
                "score": min(total_score, 100),
                "details": details
            }

        except Exception as e:
            return {
                "score": 0,
                "details": [f"Network analysis error: {str(e)}"]
            }
