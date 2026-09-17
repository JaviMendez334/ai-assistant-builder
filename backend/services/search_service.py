from backend.database.session import SessionLocal

from backend.models.chunk import Chunk
from backend.models.document import Document
from backend.models.conversation import Conversation
from backend.models.assistant import Assistant

from backend.services.embedding_service import generar_embedding


def buscar_chunks(
    pregunta: str,
    conversation_id: int,
    limite: int = 8,
    tenant_id: int = None,
    **kwargs
):
    db = SessionLocal()

    try:
        print("\n========== DIAGNÓSTICO RAG ==========")
        print("Pregunta:", pregunta)
        print("Conversation ID:", conversation_id)
        print("Tenant ID:", tenant_id)

        # Buscar la conversación
        conversacion = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

        if conversacion is None:
            print("❌ Conversación no encontrada")
            return []

        print("✅ Conversation encontrada")

        # Obtener el asistente de la conversación
        assistant = (
            db.query(Assistant)
            .filter(Assistant.id == conversacion.assistant_id)
            .first()
        )

        if assistant is None:
            print("❌ Asistente no encontrado")
            return []

        print("✅ Assistant encontrado:", assistant.id)

        # Obtener el proyecto del asistente
        project_id = assistant.project_id
        print("✅ Project ID:", project_id)

        # Obtener documentos del proyecto
        documentos = (
            db.query(Document.id)
            .filter(Document.project_id == project_id)
            .all()
        )

        documentos = [documento.id for documento in documentos]
        print("Documentos encontrados:", documentos)

        if not documentos:
            print("⚠️ No hay documentos para este proyecto")
            return []

        # Generar embedding de la pregunta
        embedding = generar_embedding(pregunta)
        print("✅ Embedding generado")

        # Construir consulta sobre los Chunks
        query = db.query(Chunk).filter(Chunk.document_id.in_(documentos))

        # Si el modelo Chunk tiene columna tenant_id, se filtra aquí
        if tenant_id is not None and hasattr(Chunk, "tenant_id"):
            query = query.filter(Chunk.tenant_id == tenant_id)

        # Buscar chunks similares por distancia coseno
        resultados = (
            query.order_by(Chunk.embedding.cosine_distance(embedding))
            .limit(limite)
            .all()
        )

        print("Chunks encontrados:", len(resultados))

        for chunk in resultados:
            print("Chunk:", chunk.id)

        return [
            {
                "id": chunk.id,
                "chunk": chunk.content,
                "score": 0,
            }
            for chunk in resultados
        ]

    finally:
        db.close()