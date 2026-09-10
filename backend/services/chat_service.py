from sqlalchemy.orm import Session
from backend.database.session import SessionLocal
from backend.models.conversation import Conversation
from backend.services.ai_engine import responder


def obtener_respuesta_asistente(
    assistant_id: int,
    mensaje: str
) -> str:
    """
    Obtiene o crea una conversación para el asistente y delega el flujo RAG/Tools a ai_engine.
    """
    db: Session = SessionLocal()
    try:
        # 1. Obtener o crear una conversación activa para el asistente
        conversacion = (
            db.query(Conversation)
            .filter(Conversation.assistant_id == assistant_id)
            .order_by(Conversation.id.desc())
            .first()
        )

        if not conversacion:
            conversacion = Conversation(
                assistant_id=assistant_id
            )
            db.add(conversacion)
            db.commit()
            db.refresh(conversacion)

        # 2. Ejecutar el pipeline de ai_engine (Historial + Tools + RAG + Guardado de mensajes)
        respuesta_texto = responder(
            conversation_id=conversacion.id,
            pregunta=mensaje
        )

        return respuesta_texto

    finally:
        db.close()
        