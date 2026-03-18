from indexer.inverted_index import inverted_index
from crawler.crawler import pages_data
import string


def search(query):
    search_engine_docs_words_mentions = {}

    clean_query = query.lower()
    clean_query = clean_query.translate(str.maketrans('', '', string.punctuation))
    query_words = clean_query.split()

    for word in query_words:
        if word in inverted_index:
            for url in inverted_index[word]:
                if url not in search_engine_docs_words_mentions:
                    search_engine_docs_words_mentions[url] = 0

                search_engine_docs_words_mentions[url] += 1

    sorted_results = sorted(
        search_engine_docs_words_mentions.items(),
        key = lambda item: item[1],
        reverse = True
    )
    
    results = []

    for url, score in sorted_results:
        result = {
            "title": pages_data[url]["title"],
            "url": url,
            "score": score
        }
        results.append(result)

    return results


if __name__ == "__main__":
    user_query = input("Qu'est ce que vous cherchez ... ")
    results = search(user_query)

    if len(results) == 0:
        print("No results found.")
    else:
        for result in results:
            print("-------------------------------------")
            print("Title :", result["title"])
            print("URL   :", result["url"])
            print("Score :", result["score"])
        print("-------------------------------------")