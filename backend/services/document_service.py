import os
import shutil

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.database.session import SessionLocal
from backend.models.chunk import Chunk  # Asegúrate de importar el modelo Chunk si no hay cascade en DB
from backend.models.document import Document
from backend.models.project import Project
from backend.services.chunk_service import guardar_chunks
from backend.services.document_processor import (
    crear_chunks,
    extraer_texto_pdf,
)

UPLOAD_FOLDER = "uploads"


def subir_documento(project_id: int, owner_id: int, file: UploadFile):
    db: Session = SessionLocal()

    try:
        proyecto = (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.owner_id == owner_id,
            )
            .first()
        )

        if proyecto is None:
            raise HTTPException(
                status_code=404,
                detail="Proyecto no encontrado",
            )

        carpeta = os.path.join(
            UPLOAD_FOLDER,
            f"project_{project_id}",
        )

        os.makedirs(carpeta, exist_ok=True)

        ruta = os.path.join(carpeta, file.filename)

        with open(ruta, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        documento = Document(
            filename=file.filename,
            filepath=ruta,
            project_id=project_id,
        )

        db.add(documento)
        db.commit()
        db.refresh(documento)

        # Extraer el texto del PDF
        texto = extraer_texto_pdf(ruta)

        # Crear los chunks
        chunks = crear_chunks(texto)

        # Guardar los chunks en la base de datos
        guardar_chunks(documento.id, chunks)

        return documento

    finally:
        db.close()


def obtener_documentos(project_id: int, owner_id: int):
    """
    Lista todos los documentos pertenecientes a un proyecto del usuario actual.
    """
    db: Session = SessionLocal()

    try:
        proyecto = (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.owner_id == owner_id,
            )
            .first()
        )

        if proyecto is None:
            return None

        documentos = (
            db.query(Document)
            .filter(Document.project_id == project_id)
            .all()
        )

        return documentos

    finally:
        db.close()


def eliminar_documento(document_id: int, owner_id: int) -> bool:
    """
    Elimina un documento de la base de datos, sus chunks y su archivo físico del disco.
    """
    db: Session = SessionLocal()

    try:
        documento = (
            db.query(Document)
            .join(Project, Document.project_id == Project.id)
            .filter(
                Document.id == document_id,
                Project.owner_id == owner_id,
            )
            .first()
        )

        if not documento:
            return False

        # 1. Borrar archivo físico del disco si existe
        if documento.filepath and os.path.exists(documento.filepath):
            try:
                os.remove(documento.filepath)
            except OSError:
                pass

        # 2. Borrar registro en BD (los chunks se eliminan si hay CASCADE o manual)
        db.delete(documento)
        db.commit()

        return True

    finally:
        db.close()
        