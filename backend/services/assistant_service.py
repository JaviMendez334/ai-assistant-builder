from backend.database.session import SessionLocal
from backend.models.assistant import Assistant
from backend.models.project import Project


def _proyecto_del_usuario(db, project_id: int, owner_id: int):
    return (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == owner_id
        )
        .first()
    )


def crear_asistente(
    project_id: int,
    owner_id: int,
    nombre: str,
    instrucciones: str,
    modelo: str
):

    db = SessionLocal()

    try:

        proyecto = _proyecto_del_usuario(
            db,
            project_id,
            owner_id
        )

        if proyecto is None:
            return None


        asistente = Assistant(
            project_id=project_id,
            nombre=nombre,
            instrucciones=instrucciones,
            modelo=modelo
        )


        db.add(asistente)
        db.commit()
        db.refresh(asistente)

        return asistente


    finally:
        db.close()



def obtener_asistentes(project_id: int, owner_id: int):

    db = SessionLocal()

    try:

        if _proyecto_del_usuario(
            db,
            project_id,
            owner_id
        ) is None:
            return None


        return (
            db.query(Assistant)
            .filter(
                Assistant.project_id == project_id
            )
            .order_by(
                Assistant.created_at.desc()
            )
            .all()
        )


    finally:
        db.close()



def obtener_asistente(
    assistant_id: int,
    owner_id: int
):

    db = SessionLocal()

    try:

        return (
            db.query(Assistant)
            .join(
                Project,
                Assistant.project_id == Project.id
            )
            .filter(
                Assistant.id == assistant_id,
                Project.owner_id == owner_id
            )
            .first()
        )


    finally:
        db.close()



def actualizar_asistente(
    assistant_id: int,
    owner_id: int,
    datos: dict
):

    db = SessionLocal()

    try:

        asistente = (
            db.query(Assistant)
            .join(
                Project,
                Assistant.project_id == Project.id
            )
            .filter(
                Assistant.id == assistant_id,
                Project.owner_id == owner_id
            )
            .first()
        )


        if asistente is None:
            return None


        for campo, valor in datos.items():
            setattr(
                asistente,
                campo,
                valor
            )


        db.commit()
        db.refresh(asistente)

        return asistente


    finally:
        db.close()



def eliminar_asistente(
    assistant_id: int,
    owner_id: int
):

    db = SessionLocal()

    try:

        asistente = (
            db.query(Assistant)
            .join(
                Project,
                Assistant.project_id == Project.id
            )
            .filter(
                Assistant.id == assistant_id,
                Project.owner_id == owner_id
            )
            .first()
        )


        if asistente is None:
            return False


        db.delete(asistente)
        db.commit()

        return True


    finally:
        db.close()
        