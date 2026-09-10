from datetime import datetime

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    titulo: str = Field(default="Nueva conversacion", min_length=1, max_length=200)


class ConversationResponse(BaseModel):
    id: int
    titulo: str
    assistant_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    contenido: str = Field(min_length=1, max_length=10000)


class MessageResponse(BaseModel):
    id: int
    role: str
    contenido: str
    conversation_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
