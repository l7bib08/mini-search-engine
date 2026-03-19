from indexer.inverted_index import inverted_index
from crawler.crawler import pages_data
import string


def search(query):
    document_scores = {}
    document_matched_words = {}

    clean_query = query.lower()
    clean_query = clean_query.translate(str.maketrans('', '', string.punctuation))
    query_words = clean_query.split()

    if len(query_words) == 0:
        return []

    for word in query_words:
        if word in inverted_index:
            for url in inverted_index[word]:
                if url not in document_scores:
                    document_scores[url] = 0
                    document_matched_words[url] = set()

                # Score de base : mot trouvé dans le document
                document_scores[url] += 1
                document_matched_words[url].add(word)

                # Bonus si le mot apparaît dans le titre
                title_text = pages_data[url]["title"].lower()
                title_text = title_text.translate(str.maketrans('', '', string.punctuation))

                if word in title_text.split():
                    document_scores[url] += 2

    # Bonus si plusieurs mots différents de la requête sont trouvés
    for url in document_scores:
        matched_count = len(document_matched_words[url])

        if matched_count >= 2:
            document_scores[url] += matched_count

        # Pénalité légère pour certaines pages moins utiles
        if "/tag/" in url or "/author/" in url:
            document_scores[url] -= 1

    sorted_results = sorted(
        document_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    results = []

    for url, score in sorted_results:
        result = {
            "title": pages_data[url]["title"],
            "url": url,
            "score": score,
            "snippet": pages_data[url]["snippet"]
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
            print("Title   :", result["title"])
            print("URL     :", result["url"])
            print("Score   :", result["score"])
            print("Snippet :", result["snippet"], "...")
        print("-------------------------------------")