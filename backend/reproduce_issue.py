from utils.helpers import clean_url

def test_clean_url():
    urls = [
        "https://www.google.com/",
        "http://example.com",
        "www.test.org/",
        "google.com"
    ]
    
    for u in urls:
        print(f"Original: {u}")
        try:
            cleaned = clean_url(u)
            print(f"Cleaned: {cleaned}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 20)

if __name__ == "__main__":
    test_clean_url()
