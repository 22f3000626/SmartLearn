import requests
import re
from bs4 import BeautifulSoup

def search_pdfs(topic, max_results=5):
    query = f"{topic} filetype:pdf"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://html.duckduckgo.com/html/?q={query}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.lower().endswith(".pdf") and "http" in href:
            title = a.get_text(strip=True)
            links.append({
                "title": title if title else href,
                "link": href
            })
        if len(links) >= max_results:
            break

    return links
