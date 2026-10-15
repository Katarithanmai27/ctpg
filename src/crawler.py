
import requests
from bs4 import BeautifulSoup
from src.url_manager import url_generator


class WebCrawler:
    """Sequential web crawler for HTML pages and JSON APIs."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch_page(self, url: str) -> requests.Response:
        """Fetch a webpage."""
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response

    def extract_data(self, response: requests.Response) -> dict:
        """Extract information from HTML or JSON responses."""

        content_type = response.headers.get("Content-Type", "").lower()

        if "application/json" in content_type:
            try:
                json_data = response.json()

                return {
                    "url": response.url,
                    "status_code": response.status_code,
                    "content_type": "JSON",
                    "title": "JSON Response",
                    "links_found": 0,
                    "response_size": len(response.content),
                    "extracted_data": json_data,
                }
            except ValueError:
                pass

        soup = BeautifulSoup(response.text, "html.parser")

        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else "No title"
        )

        return {
            "url": response.url,
            "status_code": response.status_code,
            "content_type": "HTML",
            "title": title,
            "links_found": len(soup.find_all("a")),
            "response_size": len(response.content),
            "extracted_data": soup.get_text(" ", strip=True)[:500],
        }

    def crawl(self, url: str) -> dict:
        """Crawl one URL and handle request errors."""

        try:
            response = self.fetch_page(url)
            return self.extract_data(response)

        except requests.RequestException as error:
            return {
                "url": url,
                "status_code": None,
                "content_type": "Unknown",
                "title": "Failed",
                "links_found": 0,
                "response_size": 0,
                "extracted_data": None,
                "error": str(error),
            }

    def crawl_multiple(self, urls: list[str]) -> list[dict]:
        """Crawl multiple URLs sequentially."""

        results = []

        for url in url_generator(urls):
            results.append(self.crawl(url))

        return results


if __name__ == "__main__":
    crawler = WebCrawler()

    urls = [
        "https://example.com",
        "https://httpbin.org/get",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/users/1",
    ]

    results = crawler.crawl_multiple(urls)

    for result in results:
        print("\n------------------------------")
        print("URL:", result["url"])
        print("Status Code:", result["status_code"])
        print("Type:", result["content_type"])
        print("Title:", result["title"])
        print("Links Found:", result["links_found"])
        print("Response Size:", result["response_size"], "bytes")
        print("Extracted Data:", result["extracted_data"])

        if "error" in result:
            print("Error:", result["error"])
