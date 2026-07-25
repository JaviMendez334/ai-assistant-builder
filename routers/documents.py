from fastapi import APIRouter, Depends, File, UploadFile, status

from schemas.document import DocumentResponse
from services.document_service import subir_documento
from utils.dependencies import usuario_actual

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
    return subir_documento(
        project_id,
        usuario.id,
        file,
    )

    

