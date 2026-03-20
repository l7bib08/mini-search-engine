from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search.search_engine import search

app = FastAPI()

# CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is working"}

@app.get("/search")
def search_route(q: str):
    return search(q)