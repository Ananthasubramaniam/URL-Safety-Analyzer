import argparse
import csv
import json
import logging
import os
import time
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000/api/analyze-url"
MAX_RETRIES = 2
RETRY_DELAY = 1.0  # seconds

def clean_and_validate_urls(raw_urls):
    """
    Cleans and filters a list of URLs.
    Removes duplicates, empty strings, and invalid schemes.
    """
    valid_urls = set()
    ignored_count = 0
    
    for url in raw_urls:
        url = url.strip()
        if not url:
            continue
            
        # Ignore non-http schemes
        if url.startswith(("#", "javascript:", "mailto:", "ftp:")):
            ignored_count += 1
            continue
            
        # Ensure scheme exists (default to http if missing but looks like domain)
        if not url.startswith(("http://", "https://")):
             # Simple heuristic: if it has a dot and no spaces, assume it's a domain
             if "." in url and " " not in url:
                 url = "http://" + url
             else:
                 ignored_count += 1
                 continue

        try:
            parsed = urlparse(url)
            if parsed.scheme in ("http", "https") and parsed.netloc:
                valid_urls.add(url)
            else:
                ignored_count += 1
        except Exception:
            ignored_count += 1
            
    logger.info(f"Input: {len(raw_urls)} URLs | Valid: {len(valid_urls)} | Ignored/Invalid: {ignored_count}")
    return list(valid_urls)

def analyze_single_url(url):
    """
    Sends a single URL to the analysis API with retries.
    """
    payload = {"url": url}
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "url": url,
                    "risk_score": data.get("score", 0),
                    "label": data.get("verdict", "Unknown"),
                    "error": ""
                }
            else:
                logger.warning(f"Error {response.status_code} for {url}")
        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                return {
                    "url": url,
                    "risk_score": -1,
                    "label": "Error",
                    "error": str(e)
                }
    
    return {
        "url": url,
        "risk_score": -1,
        "label": "Error",
        "error": "Max retries exceeded"
    }

def bulk_analyze(input_file, output_csv, output_json=None, batch_size=50, max_workers=5):
    """
    Main function to process URLs in bulk.
    """
    # 1. Read URLs
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return

    logger.info(f"Reading URLs from {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()
    
    urls = clean_and_validate_urls(raw_lines)
    if not urls:
        logger.error("No valid URLs found to process.")
        return

    # 2. Process Batch
    results = []
    total = len(urls)
    processed = 0
    errors = 0
    
    logger.info(f"Starting analysis of {total} URLs with {max_workers} threads...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {executor.submit(analyze_single_url, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            data = future.result()
            results.append(data)
            processed += 1
            
            if data["risk_score"] == -1:
                errors += 1
                
            # Log progress every 10 items
            if processed % 10 == 0 or processed == total:
                logger.info(f"Progress: {processed}/{total} ({processed/total*100:.1f}%) | Errors: {errors}")

    # 3. Calculate Stats
    valid_scores = [r["risk_score"] for r in results if r["risk_score"] >= 0]
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
    
    # 4. Save CSV
    logger.info(f"Saving results to {output_csv}...")
    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["url", "risk_score", "label", "error"])
            writer.writeheader()
            writer.writerows(results)
    except Exception as e:
        logger.error(f"Failed to save CSV: {e}")

    # 5. Save JSON (Optional)
    if output_json:
        logger.info(f"Saving JSON results to {output_json}...")
        try:
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")

    logger.info("="*40)
    logger.info("ANALYSIS COMPLETE")
    logger.info(f"Total: {total}")
    logger.info(f"Successful: {total - errors}")
    logger.info(f"Failed: {errors}")
    logger.info(f"Average Risk Score: {avg_score:.2f}")
    logger.info("="*40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk URL Safety Analyzer")
    parser.add_argument("input_file", help="Path to input text file containing URLs")
    parser.add_argument("--output", "-o", default="results.csv", help="Output CSV file path")
    parser.add_argument("--json-output", "-j", help="Optional output JSON file path")
    parser.add_argument("--workers", "-w", type=int, default=5, help="Number of concurrent request threads")
    
    args = parser.parse_args()
    
    try:
        # Verify API is up
        try:
             requests.get("http://localhost:8000/docs", timeout=2)
        except:
             logger.warning("Warning: Local API at http://localhost:8000 might be down. Connection refused.")

        start_time = time.time()
        bulk_analyze(args.input_file, args.output, args.json_output, max_workers=args.workers)
        logger.info(f"Time Taken: {time.time() - start_time:.2f} seconds")
        
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user.")
