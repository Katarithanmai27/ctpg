
import asyncio
import aiohttp
from bs4 import BeautifulSoup


class AsyncWebCrawler:
    """Asynchronous crawler for HTML pages and JSON APIs."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    async def fetch_page(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> dict:
        """Fetch a URL and extract useful information."""

        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:

                content = await response.text()
                content_type = response.headers.get(
                    "Content-Type", ""
                ).lower()

                if "application/json" in content_type:
                    try:
                        extracted_data = await response.json()
                        title = "JSON Response"
                        content_type_label = "JSON"
                        links_found = 0

                    except (ValueError, aiohttp.ContentTypeError):
                        extracted_data = content[:500]
                        title = "No title"
                        content_type_label = "Unknown"
                        links_found = 0

                else:
                    soup = BeautifulSoup(content, "html.parser")

                    title = (
                        soup.title.get_text(strip=True)
                        if soup.title
                        else "No title"
                    )

                    links_found = len(soup.find_all("a"))
                    extracted_data = soup.get_text(
                        " ", strip=True
                    )[:500]

                    content_type_label = "HTML"

                return {
                    "url": str(response.url),
                    "status_code": response.status,
                    "content_type": content_type_label,
                    "title": title,
                    "links_found": links_found,
                    "response_size": len(content.encode("utf-8")),
                    "extracted_data": extracted_data,
                }

        except (aiohttp.ClientError, asyncio.TimeoutError) as error:
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

    async def crawl_multiple(self, urls: list[str]) -> list[dict]:
        """Crawl multiple URLs concurrently."""

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_page(session, url)
                for url in urls
            ]

            return await asyncio.gather(*tasks)


if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/users/1",
    ]

    crawler = AsyncWebCrawler()

    results = asyncio.run(crawler.crawl_multiple(urls))

    for result in results:
        print("\n------------------------------")
        print("URL:", result["url"])
        print("Status:", result["status_code"])
        print("Type:", result["content_type"])
        print("Title:", result["title"])
        print("Links:", result["links_found"])
        print("Response size:", result["response_size"], "bytes")
        print("Extracted data:", result["extracted_data"])

        if "error" in result:
            print("Error:", result["error"])
