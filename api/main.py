from fastapi import FastAPI
from search.search_engine import search

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API is working"}


@app.get("/search")
def search_route(q: str):
    results = search(q)
    return results