# agents/rfp_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def scrape_rfp_page(url):
    """Scrape a URL and return a list of RFPs found."""
    print(f"🔍 Scraping: {url}")
    rfps = []

    try:
        html = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")

        # Try to find all <a> or <div> elements containing RFP/tender info
        for link in soup.find_all(["a", "div"], text=re.compile(r"RFP|Tender|Bid", re.I)):
            text = link.get_text(" ", strip=True)
            if len(text) < 15:
                continue

            # Try to find a due date
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})|(\d{1,2}\s+\w+\s+\d{4})", text)
            if date_match:
                raw_date = date_match.group(0)
                try:
                    due_date = datetime.strptime(raw_date, "%d %B %Y").strftime("%Y-%m-%d")
                except:
                    try:
                        due_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                    except:
                        due_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
            else:
                due_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")

            rfps.append({
                "title": text[:80],
                "description": text[:300],
                "due_date": due_date,
                "url": url
            })
        return rfps or [{"title": "No RFPs found", "description": "No matches on this page.", "due_date": "2025-12-31", "url": url}]
    except Exception as e:
        return [{"title": "Error fetching", "description": str(e), "due_date": "2025-12-31", "url": url}]
