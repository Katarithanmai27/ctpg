import requests
from bs4 import BeautifulSoup


def crawl_page(url):
    response = requests.get(url, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else "No title"

    links = soup.find_all("a")

    return {
        "url": url,
        "status_code": response.status_code,
        "title": title.strip(),
        "links_found": len(links),
        "response_size": len(response.content),
    }


if __name__ == "__main__":
    url = "https://example.com"

    result = crawl_page(url)

    print("URL:", result["url"])
    print("Status Code:", result["status_code"])
    print("Title:", result["title"])
    print("Links Found:", result["links_found"])
    print("Response Size:", result["response_size"], "bytes")