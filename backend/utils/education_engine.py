class EducationEngine:
    """
    Converts analyzer signals into educational safety tips.
    """

    TIP_MAP = {
        "ip address": "Legitimate companies rarely use raw IP addresses in links. Always prefer recognizable domain names.",
        "very new domain": "Newly registered domains are frequently used in phishing attacks. Be cautious with unfamiliar websites.",
        "recently registered": "Recently created domains may indicate temporary or malicious intent.",
        "ssl": "A missing or invalid SSL certificate means the site is not securely encrypted.",
        "entropy": "Random-looking domains are often automatically generated and may be unsafe.",
        "punycode": "Some attackers use visually similar characters to mimic trusted brands.",
        "hyphen": "Excessive hyphens in domain names are a common phishing tactic.",
        "keywords": "Urgency-related words like 'verify' or 'update' are often used to trick users.",
        "long": "Extremely long URLs may be attempting to hide malicious sections.",
        "dns": "If a domain fails DNS resolution, it may be inactive or suspicious."
    }

    GENERAL_SAFE = [
        "Always verify the sender before clicking unfamiliar links.",
        "Avoid entering credentials unless you trust the website.",
        "Check domain spelling carefully — attackers rely on small typos.",
    ]

    GENERAL_RISKY = [
        "Do not enter personal or financial information on this site.",
        "Consider reporting this URL if it was received unexpectedly.",
        "Manually type known website addresses instead of clicking links."
    ]

    def generate_tips(self, details: list[str], score: int) -> list[str]:
        tips = []

        for detail in details:
            lower_detail = detail.lower()

            for key, tip in self.TIP_MAP.items():
                if key in lower_detail:
                    tips.append(tip)

        # Add general advice based on risk level
        if score >= 70:
            tips.extend(self.GENERAL_RISKY)
        else:
            tips.extend(self.GENERAL_SAFE)

        # Remove duplicates
        return list(set(tips))
