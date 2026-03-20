from indexer.inverted_index import inverted_index
from crawler.crawler import pages_data
import string

def search(query):
    scores = {}
    matched_words = {}

    query = query.lower()
    query = query.translate(str.maketrans('', '', string.punctuation))
    words = query.split()

    for word in words:
        if word in inverted_index:
            for url in inverted_index[word]:
                if url not in scores:
                    scores[url] = 0
                    matched_words[url] = set()

                scores[url] += 1
                matched_words[url].add(word)

                # bonus titre
                title = pages_data[url]["title"].lower()
                if word in title:
                    scores[url] += 2

    # bonus multi mots
    for url in scores:
        if len(matched_words[url]) >= 2:
            scores[url] += len(matched_words[url])

    sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for url, score in sorted_results:
        results.append({
            "title": pages_data[url]["title"],
            "url": url,
            "score": score,
            "snippet": pages_data[url]["snippet"]
        })

    return results