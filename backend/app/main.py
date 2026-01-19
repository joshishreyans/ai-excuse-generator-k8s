from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.schemas import ExcuseRequest, ExcuseResponse
from app.ai_client import generate_excuse

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Backend API")
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Slow down!"}
    )

@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    return {"status": "ready"}

@app.post("/api/excuse", response_model=ExcuseResponse)
@limiter.limit("10/minute")
async def create_excuse(
    request: Request,
    req: ExcuseRequest
):
    try:
        excuse = await generate_excuse(req.tone, req.days)
        return {"excuse": excuse}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Excuse generator temporarily unavailable"
        )
