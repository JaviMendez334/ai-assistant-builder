from database.session import SessionLocal
from models.chunk import Chunk


def guardar_chunks(document_id: int, chunks: list[str]):
    db = SessionLocal()

    try:
        registros = []

        for indice, texto in enumerate(chunks):
            chunk = Chunk(
                document_id=document_id,
                chunk_index=indice,
                content=texto,
            )
            registros.append(chunk)

        db.add_all(registros)
        db.commit()

        return registros

    finally:
        db.close()

        