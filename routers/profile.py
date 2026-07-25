from fastapi import APIRouter, Depends

from schemas.user import UserResponse
from utils.dependencies import usuario_actual


router = APIRouter(prefix="/perfil", tags=["Perfil"])


@router.get("/", response_model=UserResponse)
def obtener_perfil(usuario=Depends(usuario_actual)):
    return usuario
