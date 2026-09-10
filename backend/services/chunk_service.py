from backend.database.session import SessionLocal
from backend.models.chunk import Chunk
from backend.services.embedding_service import generar_embedding


def guardar_chunks(document_id: int, chunks: list[str]):

    db = SessionLocal()

    try:
        registros = []

        for indice, texto in enumerate(chunks):

            vector = generar_embedding(texto)

            chunk = Chunk(
                document_id=document_id,
                chunk_index=indice,
                content=texto,
                embedding=vector,
            )

            registros.append(chunk)

        db.add_all(registros)
        db.commit()

        return registros

    finally:
        db.close()
        