import string
from crawler.crawler import pages_data

def tokenize_pages():
    for page in pages_data.values():
        text = page["text"].lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        
        page["words"] = words