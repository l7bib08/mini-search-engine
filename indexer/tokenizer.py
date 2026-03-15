from crawler.crawler import pages_data
import string

for page in pages_data:
    text = page["text"].lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()

    page["words"] = words