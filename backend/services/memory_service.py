from backend.database.session import SessionLocal
from backend.models.conversation import Conversation, Message

from backend.services.llm_service import cliente


LIMITE_MENSAJES = 20


def actualizar_resumen(conversation_id: int):

    db = SessionLocal()

    try:

        conversacion = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversacion is None:
            return

        mensajes = (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.asc(),
                Message.id.asc()
            )
            .all()
        )

        if len(mensajes) < LIMITE_MENSAJES:
            return

        texto = ""

        for mensaje in mensajes[:-10]:

            if mensaje.role == "user":
                texto += f"Usuario: {mensaje.contenido}\n"
            else:
                texto += f"Asistente: {mensaje.contenido}\n"

        prompt = f"""
Resume la conversación.

Conserva únicamente:

- nombres
- fechas
- decisiones
- datos importantes
- preferencias del usuario
- contexto útil

No inventes información.

Conversación:

{texto}
"""

        respuesta = cliente.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        conversacion.summary = (
            respuesta.choices[0]
            .message.content
        )

        db.commit()

    finally:
        db.close()
        