from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.schemas.user import UserCreate, UserResponse
from backend.services.user_service import autenticar_usuario, registrar_usuario
from backend.utils.jwt import crear_token


router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    nuevo_usuario = registrar_usuario(user.nombre, user.email, user.password)

    if nuevo_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya esta registrado",
        )

    return nuevo_usuario


@router.post("/login")
def login(datos: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar_usuario(datos.username, datos.password)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token(
        {"sub": str(usuario.id), "email": usuario.email, "role": usuario.role}
    )

    return {"access_token": token, "token_type": "bearer"}
