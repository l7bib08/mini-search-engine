from indexer.inverted_index import inverted_index
from crawler.crawler import pages_data
import string

search_engine_docs_words_mentions = {}

search = input("Qu'est ce que vous cherchez ... ")

clean_search = search.lower()
clean_search = clean_search.translate(str.maketrans('', '', string.punctuation))
query_words = clean_search.split()

for word in query_words:
    if word in inverted_index:
        for url in inverted_index[word]:
            if url not in search_engine_docs_words_mentions:
                search_engine_docs_words_mentions[url] = 0

            search_engine_docs_words_mentions[url] += 1

sorted_results = sorted(
    search_engine_docs_words_mentions.items(),
    key=lambda item: item[1],
    reverse=True
)

print("\nResults:\n")

if len(sorted_results) == 0:
    print("No results found.")
else:
    for url, score in sorted_results:
        title = pages_data[url]["title"]
        print("-------------------------------------")
        print("Title :", title)
        print("URL   :", url)
        print("Score :", score)

print("-------------------------------------")