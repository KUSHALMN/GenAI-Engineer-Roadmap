from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    items = [f"item_{i}" for i in range(100)]
    return {"items": items[skip: skip + limit]}

# Run: uvicorn hello_fastapi:app --reload
