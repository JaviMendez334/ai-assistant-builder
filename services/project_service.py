from database.session import SessionLocal
from models.project import Project


def crear_proyecto(nombre: str, descripcion: str | None, owner_id: int):
    db = SessionLocal()
    try:
        proyecto = Project(
            nombre=nombre,
            descripcion=descripcion,
            owner_id=owner_id,
        )
        db.add(proyecto)
        db.commit()
        db.refresh(proyecto)
        return proyecto
    finally:
        db.close()


def obtener_proyectos_por_usuario(owner_id: int):
    db = SessionLocal()
    try:
        return (
            db.query(Project)
            .filter(Project.owner_id == owner_id)
            .order_by(Project.created_at.desc())
            .all()
        )
    finally:
        db.close()


def obtener_proyecto(project_id: int, owner_id: int):
    db = SessionLocal()
    try:
        return (
            db.query(Project)
            .filter(Project.id == project_id, Project.owner_id == owner_id)
            .first()
        )
    finally:
        db.close()


def actualizar_proyecto(
    project_id: int,
    owner_id: int,
    nombre: str | None,
    descripcion: str | None,
    campos_actualizados: set[str],
):
    db = SessionLocal()
    try:
        proyecto = (
            db.query(Project)
            .filter(Project.id == project_id, Project.owner_id == owner_id)
            .first()
        )
        if proyecto is None:
            return None

        if "nombre" in campos_actualizados:
            proyecto.nombre = nombre
        if "descripcion" in campos_actualizados:
            proyecto.descripcion = descripcion

        db.commit()
        db.refresh(proyecto)
        return proyecto
    finally:
        db.close()


def eliminar_proyecto(project_id: int, owner_id: int):
    db = SessionLocal()
    try:
        proyecto = (
            db.query(Project)
            .filter(Project.id == project_id, Project.owner_id == owner_id)
            .first()
        )
        if proyecto is None:
            return False

        db.delete(proyecto)
        db.commit()
        return True
    finally:
        db.close()
