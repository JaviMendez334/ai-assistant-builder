from datetime import datetime

from backend.database.session import SessionLocal
from backend.models.assistant import Assistant
from backend.models.conversation import Conversation, Message
from backend.models.project import Project


def _asistente_del_usuario(
    db,
    assistant_id: int,
    owner_id: int,
):
    return (
        db.query(Assistant)
        .join(Project, Assistant.project_id == Project.id)
        .filter(
            Assistant.id == assistant_id,
            Project.owner_id == owner_id,
        )
        .first()
    )


def _conversacion_del_usuario(
    db,
    conversation_id: int,
    owner_id: int,
):
    return (
        db.query(Conversation)
        .join(
            Assistant,
            Conversation.assistant_id == Assistant.id,
        )
        .join(
            Project,
            Assistant.project_id == Project.id,
        )
        .filter(
            Conversation.id == conversation_id,
            Project.owner_id == owner_id,
        )
        .first()
    )


def crear_conversacion(
    assistant_id: int,
    owner_id: int,
    titulo: str,
):
    db = SessionLocal()

    try:
        if _asistente_del_usuario(
            db,
            assistant_id,
            owner_id,
        ) is None:
            return None

        conversacion = Conversation(
            assistant_id=assistant_id,
            titulo=titulo,
        )

        db.add(conversacion)
        db.commit()
        db.refresh(conversacion)

        return conversacion

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def obtener_conversaciones(owner_id: int):
    db = SessionLocal()

    try:
        return (
            db.query(Conversation)
            .join(
                Assistant,
                Conversation.assistant_id == Assistant.id,
            )
            .join(
                Project,
                Assistant.project_id == Project.id,
            )
            .filter(Project.owner_id == owner_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

    finally:
        db.close()


def obtener_conversacion(
    conversation_id: int,
    owner_id: int,
):
    db = SessionLocal()

    try:
        return _conversacion_del_usuario(
            db,
            conversation_id,
            owner_id,
        )

    finally:
        db.close()


def crear_mensaje_usuario(
    conversation_id: int,
    owner_id: int,
    contenido: str,
):
    db = SessionLocal()

    try:
        conversacion = _conversacion_del_usuario(
            db,
            conversation_id,
            owner_id,
        )

        if conversacion is None:
            return None

        if not contenido or not contenido.strip():
            return None

        mensaje = Message(
            conversation_id=conversation_id,
            role="user",
            contenido=contenido.strip(),
        )

        db.add(mensaje)

        conversacion.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(mensaje)

        return mensaje

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def crear_mensaje_asistente(
    conversation_id: int,
    contenido: str,
):
    db = SessionLocal()

    try:
        # Evitar insertar NULL en messages.contenido
        if contenido is None:
            contenido = ""

        contenido = str(contenido).strip()

        if not contenido:
            contenido = (
                "No pude generar una respuesta en este momento."
            )

        mensaje = Message(
            conversation_id=conversation_id,
            role="assistant",
            contenido=contenido,
        )

        db.add(mensaje)

        conversacion = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversacion:
            conversacion.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(mensaje)

        return mensaje

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def obtener_mensajes(
    conversation_id: int,
    owner_id: int,
):
    db = SessionLocal()

    try:
        if (
            _conversacion_del_usuario(
                db,
                conversation_id,
                owner_id,
            )
            is None
        ):
            return None

        return (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.asc(),
                Message.id.asc(),
            )
            .all()
        )

    finally:
        db.close()


def obtener_historial(conversation_id: int):
    """
    Devuelve:
    - Resumen permanente de la conversación.
    - Últimos 10 mensajes.
    """

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
            return ""

        historial = []

        if conversacion.summary:
            historial.append(
                "===== RESUMEN DE LA CONVERSACIÓN ====="
            )

            historial.append(
                conversacion.summary
            )

            historial.append("")

        historial.append(
            "===== ÚLTIMOS MENSAJES ====="
        )

        mensajes = (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.desc(),
                Message.id.desc(),
            )
            .limit(10)
            .all()
        )

        mensajes.reverse()

        for mensaje in mensajes:

            if mensaje.role == "user":
                historial.append(
                    f"Usuario: {mensaje.contenido}"
                )
            else:
                historial.append(
                    f"Asistente: {mensaje.contenido}"
                )

        return "\n".join(historial)

    finally:
        db.close()


def obtener_instrucciones(conversation_id: int):
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
            return ""

        assistant = (
            db.query(Assistant)
            .filter(
                Assistant.id == conversacion.assistant_id
            )
            .first()
        )

        if assistant is None:
            return ""

        return assistant.instrucciones

    finally:
        db.close()


def obtener_assistant_id(conversation_id: int):
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
            return None

        return conversacion.assistant_id

    finally:
        db.close()
        