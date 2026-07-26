from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CalcRequest(BaseModel):
    a: float
    b: float

@app.post("/add")
def add(req: CalcRequest):
    return {"result": req.a + req.b}

@app.post("/subtract")
def subtract(req: CalcRequest):
    return {"result": req.a - req.b}

@app.post("/multiply")
def multiply(req: CalcRequest):
    return {"result": req.a * req.b}

@app.post("/divide")
def divide(req: CalcRequest):
    if req.b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": req.a / req.b}

# Run: uvicorn calculator_api:app --reload
# Test: http://127.0.0.1:8000/docs
