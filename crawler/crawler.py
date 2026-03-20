from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

seed_url = "https://quotes.toscrape.com/"
allowed_domain = "quotes.toscrape.com"

pages_data = {}

def crawl():
    url_queue = [(seed_url, 0)]
    visited_urls = set()

    pages_crawled = 0
    max_pages = 20
    max_depth = 3

    while url_queue and pages_crawled < max_pages:
        current_url, current_depth = url_queue.pop(0)

        if current_url in visited_urls:
            continue

        print("Visiting:", current_url, "| Depth:", current_depth)
        visited_urls.add(current_url)
        pages_crawled += 1

        response = requests.get(current_url)

        if response.status_code == 200:
            page = BeautifulSoup(response.text, "html.parser")

            text_page = page.get_text()
            text_page = text_page.replace("\n", " ")
            text_page = text_page.replace("\t", " ")
            text_page = " ".join(text_page.split())

            snippet = text_page[:120]
            title_page_text = page.title.string if page.title else "No title"

            pages_data[current_url] = {
                "url": current_url,
                "depth": current_depth,
                "title": title_page_text,
                "text": text_page,
                "snippet": snippet
            }

            links = page.find_all("a")

            for link in links:
                href = link.get("href")

                if not href:
                    continue

                full_url = urljoin(current_url, href)

                # filtre bruit
                if "/tag/" in full_url or "/author/" in full_url:
                    continue

                new_depth = current_depth + 1

                if (
                    allowed_domain in full_url
                    and full_url not in visited_urls
                    and (full_url, new_depth) not in url_queue
                    and new_depth <= max_depth
                ):
                    url_queue.append((full_url, new_depth))

    print("Total pages:", len(pages_data))