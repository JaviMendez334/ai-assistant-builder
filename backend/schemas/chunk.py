from datetime import datetime

from pydantic import BaseModel


class ChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    