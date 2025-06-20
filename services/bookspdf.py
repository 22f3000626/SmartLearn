import requests
from bs4 import BeautifulSoup

def search_pdfs(topic):
    search_query = f"{topic} filetype:pdf"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    params = {
        "q": search_query
    }

    response = requests.get("https://html.duckduckgo.com/html/", params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    pdf_results = []
    for result in soup.find_all("a", href=True):
        href = result["href"]
        if href.endswith(".pdf") and len(pdf_results) < 5:
            pdf_results.append({
                "title": result.get_text(strip=True) or "PDF File",
                "link": href
            })

    return pdf_results
