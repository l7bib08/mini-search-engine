from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

seed_url = "https://quotes.toscrape.com/"
allowed_domain = "quotes.toscrape.com"

url_queue = [seed_url]
visited_urls = set()

pages_crawled = 0
max_pages = 20
max_depth = 2

while len(url_queue) != 0 and pages_crawled < max_pages:

    current_url = url_queue[0]
    url_queue.pop(0)

    if current_url not in visited_urls:
        print("Visiting:", current_url)
        visited_urls.add(current_url)
        pages_crawled += 1

        response = requests.get(current_url)

        if response.status_code == 200:
            print("page loaded successfully")

            page = BeautifulSoup(response.text, "html.parser")
            links_page = page.find_all("a")
            text_page = page.get_text()
            title_page_text = page.title.string

            for link in links_page:
                href = link.get("href")

                if href is None:
                    continue

                full_url = urljoin(current_url, href)

                if allowed_domain in full_url and full_url not in visited_urls and full_url not in url_queue:
                    url_queue.append(full_url)

                print("Full link:", full_url)

        else:
            print("page failed")