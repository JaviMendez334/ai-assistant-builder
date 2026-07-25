from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        