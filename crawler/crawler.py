from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

seed_url = "https://quotes.toscrape.com/"
allowed_domain = "quotes.toscrape.com"

url_queue = [(seed_url, 0)]
visited_urls = set()
pages_data = []

pages_crawled = 0
max_pages = 20
max_depth = 3

while len(url_queue) != 0 and pages_crawled < max_pages:

    current_url, current_depth = url_queue.pop(0)

    if current_url in visited_urls:
        continue

    print("Visiting:", current_url, "| Depth:", current_depth)
    visited_urls.add(current_url)
    pages_crawled += 1

    response = requests.get(current_url)

    if response.status_code == 200:
        print("Page loaded successfully")

        page = BeautifulSoup(response.text, "html.parser")
        links_page = page.find_all("a")
        text_page = page.get_text()
        text_page = text_page.replace("\n", " ")
        text_page = text_page.replace("\t", " ")
        text_page = " ".join(text_page.split())
        title_page_text = page.title.string if page.title else "No title"

        page_record = {
            "url": current_url,
            "depth": current_depth,
            "title": title_page_text,
            "text": text_page
        }

        pages_data.append(page_record)

        valid_links_count = 0

        print("-------------------------------------")
        print("URL:", current_url)
        print("Depth:", current_depth)
        print("Title:", title_page_text)
        print("Text length:", len(text_page))

        for link in links_page:
            href = link.get("href")

            if href is None:
                continue

            full_url = urljoin(current_url, href)
            new_depth = current_depth + 1
            valid_links_count += 1

            if (
                allowed_domain in full_url
                and full_url not in visited_urls
                and (full_url, new_depth) not in url_queue
                and new_depth <= max_depth
            ):
                url_queue.append((full_url, new_depth))

            print("Full link:", full_url, "| New depth:", new_depth)

        print("Links found:", valid_links_count)
        print("-------------------------------------")

    else:
        print("Page failed with status code:", response.status_code)

print("Total stored pages:", len(pages_data))