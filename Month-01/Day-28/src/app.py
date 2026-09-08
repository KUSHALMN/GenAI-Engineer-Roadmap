from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

try:
    from .firewall import SecurityFirewall
except ImportError:
    from firewall import SecurityFirewall

app = FastAPI(title="GenAI Security Firewall - Day 28")
firewall = SecurityFirewall()

class InspectRequest(BaseModel):
    prompt: str = Field(..., min_length=1)

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 28: GenAI Security"}

@app.post("/api/v1/security/inspect")
def inspect_request(req: InspectRequest):
    result = firewall.inspect_prompt(req.prompt)
    if not result["is_safe"]:
        raise HTTPException(status_code=403, detail={"threat": result})
    return result

@app.post("/api/v1/security/verify_output")
def verify_output(payload: Dict[str, str]):
    completion = payload.get("completion", "")
    if firewall.inspect_completion_for_leak(completion):
        raise HTTPException(status_code=500, detail={"error": "Canary token exfiltration detected!"})
    return {"status": "clean"}
