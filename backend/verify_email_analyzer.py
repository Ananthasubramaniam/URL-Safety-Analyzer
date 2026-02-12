import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Monkeypatch LogisticRegression to handle missing multi_class attribute
try:
    from sklearn.linear_model import LogisticRegression
    if not hasattr(LogisticRegression, 'multi_class'):
        print("Monkeypatching LogisticRegression...")
        # Add a dummy property or attribute
        setattr(LogisticRegression, 'multi_class', 'auto') 
except ImportError:
    pass

try:
    from analyzers.email_analyzer import EmailAnalyzer
    print("EmailAnalyzer imported successfully.")
except Exception as e:
    print(f"Failed to import EmailAnalyzer: {e}")
    sys.exit(1)

try:
    analyzer = EmailAnalyzer()
    print("EmailAnalyzer instantiated successfully.")
except Exception as e:
    print(f"Failed to instantiate EmailAnalyzer: {e}")
    sys.exit(1)

subject = "Test Subject"
body = "This is a test email body."

try:
    result = analyzer.analyze(subject, body)
    print("Analysis successful!")
    print(result)
except Exception as e:
    print(f"Analysis failed: {e}")
    sys.exit(1)
