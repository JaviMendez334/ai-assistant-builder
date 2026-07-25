from fastapi import APIRouter, Depends, HTTPException, status

from schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from services.project_service import (
    actualizar_proyecto,
    crear_proyecto,
    eliminar_proyecto,
    obtener_proyecto,
    obtener_proyectos_por_usuario,
)
from utils.dependencies import usuario_actual


router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def crear_nuevo_proyecto(
    datos: ProjectCreate,
    usuario=Depends(usuario_actual),
):
    return crear_proyecto(datos.nombre, datos.descripcion, usuario.id)


@router.get("/", response_model=list[ProjectResponse])
def listar_proyectos(usuario=Depends(usuario_actual)):
    return obtener_proyectos_por_usuario(usuario.id)


@router.get("/{project_id}", response_model=ProjectResponse)
def ver_proyecto(project_id: int, usuario=Depends(usuario_actual)):
    proyecto = obtener_proyecto(project_id, usuario.id)
    if proyecto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return proyecto


@router.put("/{project_id}", response_model=ProjectResponse)
def editar_proyecto(
    project_id: int,
    datos: ProjectUpdate,
    usuario=Depends(usuario_actual),
):
    campos_actualizados = datos.model_fields_set
    if not campos_actualizados:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Debes enviar al menos un campo para actualizar",
        )

    proyecto = actualizar_proyecto(
        project_id,
        usuario.id,
        datos.nombre,
        datos.descripcion,
        campos_actualizados,
    )
    if proyecto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return proyecto


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_proyecto(project_id: int, usuario=Depends(usuario_actual)):
    if not eliminar_proyecto(project_id, usuario.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
