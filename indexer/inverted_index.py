from crawler.crawler import crawl, pages_data
from indexer.tokenizer import tokenize_pages

crawl()
tokenize_pages()

inverted_index = {}

for url, page in pages_data.items():
    unique_words = set(page["words"])

    for word in unique_words:
        if word not in inverted_index:
            inverted_index[word] = []

        inverted_index[word].append(url)

print("Number of indexed words:", len(inverted_index))

for word, urls in list(inverted_index.items())[:10]:
    print(word, "->", urls)