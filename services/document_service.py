import os
import shutil

from fastapi import HTTPException, UploadFile

from database.session import SessionLocal
from models.document import Document
from models.project import Project
from services.chunk_service import guardar_chunks
from services.document_processor import (
    crear_chunks,
    extraer_texto_pdf,
)

UPLOAD_FOLDER = "uploads"


def subir_documento(project_id: int, owner_id: int, file: UploadFile):
    db = SessionLocal()

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
        