from fastapi import FastAPI
from config import APP_TITLE, APP_VERSION
from database import create_tables
from routes import router

app = FastAPI(title=APP_TITLE, version=APP_VERSION)
app.include_router(router)

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def root():
    return {"message": f"{APP_TITLE} is running!"}

# Run: uvicorn app:app --reload
# Docs: http://127.0.0.1:8000/docs
