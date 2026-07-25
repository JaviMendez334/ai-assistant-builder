from fastapi import APIRouter, Depends, HTTPException, status

from schemas.assistant import AssistantCreate, AssistantResponse, AssistantUpdate
from services.assistant_service import (
    actualizar_asistente,
    crear_asistente,
    eliminar_asistente,
    obtener_asistente,
    obtener_asistentes,
)
from utils.dependencies import usuario_actual


router = APIRouter(prefix="/asistentes", tags=["Asistentes"])


@router.post(
    "/proyecto/{project_id}",
    response_model=AssistantResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_nuevo_asistente(
    project_id: int,
    datos: AssistantCreate,
    usuario=Depends(usuario_actual),
):
    asistente = crear_asistente(
        project_id,
        usuario.id,
        datos.nombre,
        datos.instrucciones,
        datos.modelo,
    )
    if asistente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return asistente


@router.get("/proyecto/{project_id}", response_model=list[AssistantResponse])
def listar_asistentes(project_id: int, usuario=Depends(usuario_actual)):
    asistentes = obtener_asistentes(project_id, usuario.id)
    if asistentes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return asistentes


@router.get("/{assistant_id}", response_model=AssistantResponse)
def ver_asistente(assistant_id: int, usuario=Depends(usuario_actual)):
    asistente = obtener_asistente(assistant_id, usuario.id)
    if asistente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistente no encontrado")
    return asistente


@router.put("/{assistant_id}", response_model=AssistantResponse)
def editar_asistente(
    assistant_id: int,
    datos: AssistantUpdate,
    usuario=Depends(usuario_actual),
):
    campos = datos.model_dump(exclude_unset=True)
    if not campos:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Debes enviar al menos un campo para actualizar",
        )
    asistente = actualizar_asistente(assistant_id, usuario.id, campos)
    if asistente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistente no encontrado")
    return asistente


@router.delete("/{assistant_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_asistente(assistant_id: int, usuario=Depends(usuario_actual)):
    if not eliminar_asistente(assistant_id, usuario.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistente no encontrado")
