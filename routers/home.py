from fastapi import APIRouter, Depends, HTTPException, status

from schemas.user import User, UserResponse
from services.user_service import (
    actualizar_usuario,
    eliminar_usuario,
    obtener_usuario_por_id,
    obtener_usuarios,
)
from utils.dependencies import requerir_administrador


router = APIRouter()


@router.get("/")
def home():
    return {"mensaje": "Bienvenido a AI Assistant Builder"}


@router.get("/saludar/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola {nombre}, bienvenido a AI Assistant Builder"}


@router.get("/despedir/{nombre}")
def despedir(nombre: str):
    return {"mensaje": f"Hasta luego {nombre}"}


@router.get("/usuarios", response_model=list[UserResponse])
def listar_usuarios(usuario_admin=Depends(requerir_administrador)):
    return obtener_usuarios()


@router.get("/usuarios/{id}", response_model=UserResponse)
def obtener_usuario(id: int, usuario_admin=Depends(requerir_administrador)):
    usuario = obtener_usuario_por_id(id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario


@router.put("/usuarios/{id}", response_model=UserResponse)
def editar_usuario(id: int, user: User, usuario_admin=Depends(requerir_administrador)):
    usuario = actualizar_usuario(id, user.nombre)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario


@router.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_usuario(id: int, usuario_admin=Depends(requerir_administrador)):
    if eliminar_usuario(id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
