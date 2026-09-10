from fastapi import APIRouter, Depends, HTTPException, status

from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from backend.services.chat_service import (
    obtener_respuesta_asistente,
)
from backend.utils.dependencies import usuario_actual


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/{assistant_id}",
    response_model=ChatResponse
)
def chat_asistente(
    assistant_id: int,
    datos: ChatRequest,
    usuario=Depends(usuario_actual),
):
    respuesta = obtener_respuesta_asistente(
        assistant_id,
        datos.mensaje
    )

    if respuesta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asistente no encontrado"
        )

    return {
        "respuesta": respuesta
    }
