# PhishGuard – URL Safety Analyzer

**Team Name:** The Final Commit  
**Team Members:**  
Ananthasubramaniam  
Arvind Srikanth  
Deepak Kumar Patro  

## 1. Problem Statement
Phishing attacks remain one of the most widespread and damaging forms of cybercrime. Malicious URLs are often crafted to mimic legitimate websites, tricking users into revealing sensitive information such as login credentials, financial data, and personal identity details.

These attacks lead to:
- Financial fraud
- Identity theft
- Data breaches
- Reputational damage
- Enterprise-level security incidents

Traditional detection methods often rely solely on blacklist databases, which are reactive and may fail to detect newly registered malicious domains. Users also lack real-time awareness about why a URL is dangerous.

There is a need for an intelligent, explainable, and real-time URL analysis system that not only detects threats but also educates users.

## 2. Our Solution
PhishGuard – URL Safety Analyzer is a real-time phishing detection and awareness platform that evaluates URLs using a multi-layered detection pipeline.

Instead of relying on a single method, PhishGuard combines:
- Pattern-based heuristic analysis
- Machine Learning classification
- Network-level validation (WHOIS, SSL, DNS checks)
- External threat intelligence APIs (e.g., VirusTotal, Google Safe Browsing)
- Structured risk scoring engine
- Educational safety recommendations

### Detection Approach

#### Pattern Analysis
- Suspicious keywords detection
- Excessive URL length
- IP address usage instead of domain
- Unusual symbols (e.g., '@')
- Suspicious file extensions
- Subdomain complexity

#### Machine Learning Classification
- Extracted URL features are passed to a trained phishing detection model
- Model outputs a probability score
- Converted into a normalized risk contribution

#### Network Validation
- Domain age verification via WHOIS
- SSL certificate validation
- DNS-level validation

#### Threat Intelligence APIs
- Integration with VirusTotal (if configured)
- Google Safe Browsing blacklist checks
- Real-time blacklist override for known malicious domains

#### Risk Scoring Engine
- Weighted aggregation of multiple signals
- Normalized final score (0–100)
- Clear verdict classification

#### User Awareness Tips
- Context-based recommendations
- Explainable threat reasoning

## 3. Core Features
- Real-time URL scanning
- Multi-layer risk classification (Safe / Suspicious / Phishing)
- Detailed structured threat report
- Score breakdown (Pattern, ML, Network, API)
- Phishing awareness suggestions
- External threat intelligence integration
- Secure ORM-based database logging
- Clean and explainable scoring methodology
- **Chrome Extension**: Real-time protection while browsing.
- **Bulk Analysis**: Scan multiple URLs via file upload or CLI.
- **Analytics Dashboard**: Visual insights into threat history.
- **History Management**: Full control to clear scan data.

## 4. System Architecture

### High-Level Flow
Frontend (React)  
→ FastAPI Backend  
→ Pattern Analyzer  
→ ML Analyzer  
→ Network Analyzer  
→ External API Checks  
→ Scoring Engine  
→ Structured Risk Report

### Backend Components
**analyzers/**
- pattern_analyzer.py
- ml_analyzer.py
- network_analyzer.py
- blacklist_analyzer.py

**utils/**
- scoring_engine.py
- feature_extractor.py

**routers/**
- url_routes.py
- dashboard_routes.py
- email_routes.py

**scripts/**
- bulk_analyze.py

**Database:**
- SQLAlchemy ORM
- SQLite (threats.db)

## 5. Tech Stack

### Frontend
- React (Vite)
- JavaScript
- HTML5
- CSS3

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy ORM

### APIs
- VirusTotal API
- Google Safe Browsing API

### Database
- SQLite (local persistent storage)

### Libraries & Tools
- python-dotenv
- joblib
- scikit-learn
- requests
- whois

## 6. How to Run the Project

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip
- npm
- VirusTotal API Key (optional but recommended)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/PhishGuard.git
   cd PhishGuard/backend
   ```
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # or
   source venv/bin/activate   # macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create environment file:
   ```bash
   copy .env.example .env
   ```
5. Edit `.env` and add:
   ```env
   VIRUSTOTAL_API_KEY=your_api_key_here
   GOOGLE_SAFE_KEY=your_api_key_here
   DATABASE_URL=sqlite:///backend/threats.db
   ```
6. Run backend:
   ```bash
   uvicorn main:app --reload
   ```
   Backend will run at: http://127.0.0.1:8000

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run frontend:
   ```bash
   npm run dev
   ```
   Frontend will run at: http://localhost:5173

### Chrome Extension Setup
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked** and select the `extension/` directory.
4. The extension will now protect you in real-time!

### Bulk Analysis Tool
- **CLI**: Run `python backend/bulk_analyze.py urls.txt`
- **Web**: Access the **Bulk Scan** tab in the dashboard.

## 7. Learnings & Challenges During the Hackathon

Genuine Learnings and Challenges Faced During the Hackathon

One of the main challenges we faced was collaborating using Git. Since this was our first hands-on experience working in a team environment with version control, the workflow initially felt difficult and unfamiliar. However, we applied what we had learned in the MLSD course, using Git commands to manage repositories, track changes, and coordinate our work effectively.

Implementing machine learning algorithms was another significant challenge. Moving from theoretical understanding to practical implementation required deeper problem-solving and experimentation. Through this process, we learned how to apply models in real-time scenarios and gained a clearer understanding of their real-world use cases. The concepts and models we studied in our machine learning course proved to be especially helpful in guiding our approach.

### Key Learnings
- Security tools must themselves follow strict security hygiene
- Stability and structure matter more than feature count


## 8. Demo
- **Demo Video:** (Add link here)

## 9. Project Structure
```text
├── backend/
│   ├── analyzers/
│   ├── routers/
│   ├── utils/
│   ├── models/
│   ├── main.py
│   ├── bulk_analyze.py
│   └── threats.db
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   └── package.json
│
├── extension/
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html
│   ├── popup.js
│   └── popup.css
│
├── .env.example
├── requirements.txt
└── README.md
```

### Security Considerations

- API keys stored securely using environment variables
- Sensitive files excluded via .gitignore
- No hardcoded credentials

### Future Enhancements
- Email attachment scanner (Enhanced)
- QR code safety checker
- Advanced anomaly detection models

PhishGuard demonstrates a layered, explainable, and scalable approach to phishing detection, combining traditional heuristics with machine learning and external intelligence sources to deliver real-time URL risk assessment.
