from datetime import datetime

from pydantic import BaseModel, Field


class AssistantCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    instrucciones: str = Field(min_length=1, max_length=10000)
    modelo: str = Field(default="gpt-4.1-mini", min_length=1, max_length=100)


class AssistantUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    instrucciones: str | None = Field(default=None, min_length=1, max_length=10000)
    modelo: str | None = Field(default=None, min_length=1, max_length=100)
    activo: bool | None = None


class AssistantResponse(BaseModel):
    id: int
    nombre: str
    instrucciones: str
    modelo: str
    activo: bool
    project_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
