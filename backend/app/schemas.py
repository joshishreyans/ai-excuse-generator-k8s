from pydantic import BaseModel, Field

class ExcuseRequest(BaseModel):
    tone: str = Field(..., example="funny")
    days: int = Field(..., ge=1, le=30)

class ExcuseResponse(BaseModel):
    excuse: str
