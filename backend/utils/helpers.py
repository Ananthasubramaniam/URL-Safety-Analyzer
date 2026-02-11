import re
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """Checks if a URL has a valid structure."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def clean_url(url: str) -> str:
    """Removes http/https and www for cleaner analysis."""
    url = url.replace("https://", "").replace("http://", "")
    url = url.replace("www.", "")
    if url.endswith("/"):
        url = url[:-1]
    return url

def get_domain(url: str) -> str:
    """Extracts domain from URL."""
    try:
        result = urlparse(url)
        return result.netloc
    except:
        return ""
