from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.prompt import build_user_prompt
from app.llm import generate_excuse

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="AI Excuse Generator")
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Slow down 🙂"}
    )

class ExcuseRequest(BaseModel):
    tone: str = Field(..., example="funny")
    days: int = Field(..., ge=1, le=30)

@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    return {"status": "ready"}

@app.post("/generate")
@limiter.limit("5/minute")
def generate(request: Request, req: ExcuseRequest):
    try:
        prompt = build_user_prompt(req.tone, req.days)
        excuse = generate_excuse(prompt)
        return {"excuse": excuse}
    except Exception as e:
        # TEMP DEBUG — REMOVE LATER
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))