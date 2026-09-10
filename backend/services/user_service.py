from backend.database.session import SessionLocal
from backend.models.user import User
from backend.utils.security import encriptar_password, verificar_password


def crear_usuario(nombre: str):
    db = SessionLocal()
    try:
        nuevo_usuario = User(nombre=nombre)
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    finally:
        db.close()


def obtener_usuarios():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()


def obtener_usuario_por_id(id: int):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == id).first()
    finally:
        db.close()


def actualizar_usuario(id: int, nombre: str):
    db = SessionLocal()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if usuario is None:
            return None

        usuario.nombre = nombre
        db.commit()
        db.refresh(usuario)
        return usuario
    finally:
        db.close()


def eliminar_usuario(id: int):
    db = SessionLocal()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if usuario is None:
            return None

        db.delete(usuario)
        db.commit()
        return True
    finally:
        db.close()


def registrar_usuario(nombre: str, email: str, password: str):
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            return None

        nuevo_usuario = User(
            nombre=nombre,
            email=email,
            password=encriptar_password(password),
            role="user",
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    finally:
        db.close()


def autenticar_usuario(email: str, password: str):
    db = SessionLocal()
    try:
        usuario = db.query(User).filter(User.email == email).first()
        if usuario is None or not verificar_password(password, usuario.password):
            return None
        return usuario
    finally:
        db.close()
