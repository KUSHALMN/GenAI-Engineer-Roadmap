"""
main.py — FastAPI entrypoint for LangChain Agent API.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from inference import run_agent
from schemas import AgentResponse

app = FastAPI(title="LangChain Agent API", version="1.0.0")


class QueryRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/agent/run", response_model=AgentResponse)
def agent_run(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return run_agent(request.query)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
