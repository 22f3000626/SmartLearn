import requests

def search_books(topic):
    url = f"https://www.googleapis.com/books/v1/volumes?q={topic}"
    response = requests.get(url).json()
    books = []
    for item in response.get("items", [])[:5]:
        books.append({
            "title": item["volumeInfo"].get("title", "No Title"),
            "link": item["volumeInfo"].get("infoLink", "#")
        })
    return books
