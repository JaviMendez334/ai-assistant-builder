from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: str | None = Field(default=None, max_length=5000)


class ProjectUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    descripcion: str | None = Field(default=None, max_length=5000)


class ProjectResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
