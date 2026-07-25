from fastapi import APIRouter, Depends, HTTPException, status

from schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from services.conversation_service import (
    crear_conversacion,
    crear_mensaje_usuario,
    obtener_conversacion,
    obtener_conversaciones,
    obtener_mensajes,
)
from utils.dependencies import usuario_actual


router = APIRouter(prefix="/conversaciones", tags=["Conversaciones"])


@router.post(
    "/asistente/{assistant_id}",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_nueva_conversacion(
    assistant_id: int,
    datos: ConversationCreate,
    usuario=Depends(usuario_actual),
):
    conversacion = crear_conversacion(assistant_id, usuario.id, datos.titulo)
    if conversacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistente no encontrado")
    return conversacion


@router.get("/", response_model=list[ConversationResponse])
def listar_conversaciones(usuario=Depends(usuario_actual)):
    return obtener_conversaciones(usuario.id)


@router.get("/{conversation_id}", response_model=ConversationResponse)
def ver_conversacion(conversation_id: int, usuario=Depends(usuario_actual)):
    conversacion = obtener_conversacion(conversation_id, usuario.id)
    if conversacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversacion no encontrada")
    return conversacion


@router.post(
    "/{conversation_id}/mensajes",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def enviar_mensaje(
    conversation_id: int,
    datos: MessageCreate,
    usuario=Depends(usuario_actual),
):
    mensaje = crear_mensaje_usuario(conversation_id, usuario.id, datos.contenido)
    if mensaje is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversacion no encontrada")
    return mensaje


@router.get("/{conversation_id}/mensajes", response_model=list[MessageResponse])
def listar_mensajes(conversation_id: int, usuario=Depends(usuario_actual)):
    mensajes = obtener_mensajes(conversation_id, usuario.id)
    if mensajes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversacion no encontrada")
    return mensajes
