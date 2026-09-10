from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from backend.services.ai_engine import responder
from backend.services.llm_service import generar_respuesta_stream
from backend.services.memory_service import actualizar_resumen

from backend.services.conversation_service import (
    crear_conversacion,
    crear_mensaje_usuario,
    crear_mensaje_asistente,
    obtener_conversacion,
    obtener_conversaciones,
    obtener_mensajes,
    obtener_historial,
    obtener_instrucciones,
)

from backend.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)

from backend.utils.dependencies import usuario_actual


router = APIRouter(
    prefix="/conversaciones",
    tags=["Conversaciones"],
)


# ============================================================
# CREAR CONVERSACIÓN
# ============================================================

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
    conversacion = crear_conversacion(
        assistant_id,
        usuario.id,
        datos.titulo,
    )

    if conversacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asistente no encontrado",
        )

    return conversacion


# ============================================================
# LISTAR CONVERSACIONES
# ============================================================

@router.get(
    "/",
    response_model=list[ConversationResponse],
)
def listar_conversaciones(
    usuario=Depends(usuario_actual),
):
    return obtener_conversaciones(usuario.id)


# ============================================================
# VER UNA CONVERSACIÓN
# ============================================================

@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def ver_conversacion(
    conversation_id: int,
    usuario=Depends(usuario_actual),
):
    conversacion = obtener_conversacion(
        conversation_id,
        usuario.id,
    )

    if conversacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada",
        )

    return conversacion


# ============================================================
# ENVIAR MENSAJE
# ============================================================

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
    mensaje_usuario = crear_mensaje_usuario(
        conversation_id,
        usuario.id,
        datos.contenido,
    )

    if mensaje_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada",
        )

    respuesta = responder(
        conversation_id=conversation_id,
        pregunta=datos.contenido,
    )

    mensaje_asistente = crear_mensaje_asistente(
        conversation_id,
        respuesta,
    )

    actualizar_resumen(
        conversation_id
    )

    return mensaje_asistente


# ============================================================
# ENVIAR MENSAJE EN STREAMING
# ============================================================

@router.post(
    "/{conversation_id}/stream",
)
def enviar_mensaje_stream(
    conversation_id: int,
    datos: MessageCreate,
    usuario=Depends(usuario_actual),
):
    mensaje_usuario = crear_mensaje_usuario(
        conversation_id,
        usuario.id,
        datos.contenido,
    )

    if mensaje_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada",
        )

    historial = obtener_historial(
        conversation_id
    )

    instrucciones = obtener_instrucciones(
        conversation_id
    )

    def generar():
        respuesta_completa = ""

        for token in generar_respuesta_stream(
            pregunta=datos.contenido,
            contexto="",
            historial=historial,
            instrucciones=instrucciones,
        ):
            respuesta_completa += token

            yield token

        crear_mensaje_asistente(
            conversation_id,
            respuesta_completa,
        )

        actualizar_resumen(
            conversation_id
        )

    return StreamingResponse(
        generar(),
        media_type="text/plain",
    )


# ============================================================
# LISTAR MENSAJES
# ============================================================

@router.get(
    "/{conversation_id}/mensajes",
    response_model=list[MessageResponse],
)
def listar_mensajes(
    conversation_id: int,
    usuario=Depends(usuario_actual),
):
    mensajes = obtener_mensajes(
        conversation_id,
        usuario.id,
    )

    if mensajes is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada",
        )

    return mensajes
