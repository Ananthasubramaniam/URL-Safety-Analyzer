import re
from urllib.parse import urlparse
from .helpers import get_domain

class FeatureExtractor:
    """Extracts numerical features from a URL for ML models."""
    
    def extract_features(self, url: str):
        features = {}
        
        # 1. Length Features
        features['url_length'] = len(url)
        features['domain_length'] = len(get_domain(url))
        
        # 2. Count Features
        features['dot_count'] = url.count('.')
        features['hyphen_count'] = url.count('-')
        features['at_count'] = url.count('@')
        features['qmark_count'] = url.count('?')
        features['amp_count'] = url.count('&')
        features['digit_count'] = sum(c.isdigit() for c in url)
        
        # 3. Boolean Features
        features['has_https'] = 1 if url.startswith('https') else 0
        features['has_ip_address'] = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0
        
        # Return as list for model prediction (order matters!)
        return [
            features['url_length'],
            features['domain_length'],
            features['dot_count'],
            features['hyphen_count'],
            features['at_count'],
            features['qmark_count'],
            features['amp_count'],
            features['digit_count'],
            features['has_https'],
            features['has_ip_address']
        ]
