# URL Safety Analyzer

## Overview
URL Safety Analyzer is a professional-grade security tool designed to identify and mitigate phishing and malicious URL threats. The system provides automated, multi-dimensional analysis of web resources, delivering a structured risk assessment and actionable safety recommendations to protect users from credential harvesting, malware distribution, and social engineering attacks.

## Key Features
- Pattern-based detection: Heuristic analysis of URL strings for suspicious indicators such as punycode, high entropy, and keyword abuse.
- ML-based classification: Machine learning modeling of URL features to predict the probability of a phishing attempt.
- Network validation: Real-time verification of DNS resolution, domain age via WHOIS data, and SSL certificate validity.
- External API integration: Support for cross-referencing URLs against established threat intelligence blacklists.
- Risk scoring engine: A weighted aggregation system that synthesizes multiple data points into a single normalized safety score.
- Educational recommendations: Generation of deterministic, rule-based safety advice based on specific risk indicators.
- Structured risk report: Comprehensive JSON-formatted output providing score, verdict, and detailed analysis breakdown.

## System Architecture
The application is built on a decoupled full-stack architecture focusing on performance and modularity.

- Frontend (React): A modern, responsive user interface built with Vite, providing a clean dashboard for inputting resources and visualizing structured risk reports.
- Backend (FastAPI): A high-performance asynchronous API server that handles request orchestration, analysis execution, and asynchronous reporting.
- Analyzers:
  - PatternAnalyzer: Implements string-level heuristics and entropy calculations.
  - ML Analyzer: Utilizes a pre-trained classification model for predictive threat modeling.
  - NetworkChecker: Manages external network probes and validation logic.
- Scoring Engine: A dedicated utility that handles the normalization and weighting of raw signals from different analysis modules.
- Database (SQLAlchemy + SQLite): Provides persistent storage for scan history using an Object-Relational Mapper (ORM).
- External APIs: Interfaces with third-party geolocation and threat intelligence providers.

## Detection Pipeline
1. Input: User submits a URL via the frontend dashboard or API endpoint.
2. Pattern analysis: The system evaluates the URL structure for common phishing tactics.
3. ML probability scoring: Feature extraction is performed, and data is fed into the ML classifier.
4. Network checks: The backend performs DNS, WHOIS, and SSL validation.
5. External blacklist check: The URL is verified against known malicious repositories.
6. Score aggregation: The Scoring Engine weights all signals to produce a final risk assessment.
7. Risk report generation: A structured report containing the verdict, breakdown, and recommendations is compiled and returned.

## Risk Scoring Methodology
PhishGuard utilizes a weighted scoring system to ensure accuracy and explainability. Each analyzer (Pattern, ML, Network) contributes a partial score, which is then weighted according to its confidence level (e.g., Network safety typically holds higher weight for legitimacy verification). Critical indicators, such as a confirmed blacklist match, can override standard weights to ensure immediate isolation of high-risk threats.

## Security Considerations
- Parameterized ORM queries: All database interactions utilize SQLAlchemy to prevent SQL injection vulnerabilities.
- Environment variable configuration: Sensitive configurations and API keys are managed via .env files, never hardcoded in the source.
- Error handling strategy: The system implements an error-masking strategy, catching internal exceptions and returning graceful fallback responses to ensure no stack traces or sensitive system info is exposed to the client.
- API isolation: External network calls are performed with strict timeouts to prevent resource exhaustion and ensure system stability.

## Environment Configuration
The application uses environment variables to manage sensitive configuration and API keys.

1.  Copy the example environment file: `cp .env.example .env` (or manually copy in file explorer).
2.  Open `.env` and provide your specific API keys:
    -   `GOOGLE_SAFE_KEY`: Your Google Safe Browsing API key.
    -   `DATABASE_URL`: Path to the SQLite database (default: `sqlite:///threats.db`).

Environment variables are used to ensure that secrets are not committed to version control. The `.env` file is explicitly ignored in `.gitignore` and must be managed locally.

## Installation & Setup

### Backend
1. Navigate to the backend directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac).
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file from the provided template.
6. Start the server: `python main.py`

### Frontend
1. Navigate to the frontend directory.
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

## API Endpoint

POST /api/analyze-url

Example Request:
```json
{
  "url": "http://suspicious-verification-update.com/login"
}
```

Example Response:
```json
{
  "score": 78,
  "verdict": "Phishing / Unsafe",
  "breakdown": {
    "pattern": 35,
    "ml": 18,
    "network": 25
  },
  "reasons": [
    "High digit density in URL",
    "URL does not use HTTPS",
    "WHOIS lookup failed or hidden"
  ],
  "recommendations": [
    "Do not enter personal or financial information on this site.",
    "A missing or invalid SSL certificate means the site is not securely encrypted.",
    "Newly registered domains are frequently used in phishing attacks."
  ],
  "ml_probability": 0.62
}
```

## Future Enhancements
- Integration with distributed threat intelligence networks.
- Implementation of safe browser sandboxing for dynamic content analysis.
- Expansion of the pattern-based detection library for zero-day threat variants.
- Support for deep-packet inspection of network-level traffic signals.