from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from backend.schemas.document import DocumentResponse
from backend.services.document_service import (
    eliminar_documento,
    obtener_documentos,
    subir_documento,
)
from backend.utils.dependencies import usuario_actual

router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"],
)


@router.post(
    "/{project_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def subir_archivo(
    project_id: int,
    file: UploadFile = File(...),
    usuario=Depends(usuario_actual),
):
    documento = subir_documento(
        project_id,
        usuario.id,
        file,
    )

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo procesar el documento o proyecto no encontrado",
        )

    return documento


@router.get(
    "/{project_id}",
    response_model=list[DocumentResponse],
)
def listar_archivos(
    project_id: int,
    usuario=Depends(usuario_actual),
):
    documentos = obtener_documentos(
        project_id,
        usuario.id,
    )

    if documentos is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    return documentos


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def borrar_archivo(
    document_id: int,
    usuario=Depends(usuario_actual),
):
    eliminado = eliminar_documento(
        document_id,
        usuario.id,
    )

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado",
        )
    