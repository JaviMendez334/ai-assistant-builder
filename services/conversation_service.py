from database.session import SessionLocal
from models.assistant import Assistant
from models.conversation import Conversation, Message
from models.project import Project


def _asistente_del_usuario(db, assistant_id: int, owner_id: int):
    return (
        db.query(Assistant)
        .join(Project, Assistant.project_id == Project.id)
        .filter(Assistant.id == assistant_id, Project.owner_id == owner_id)
        .first()
    )


def _conversacion_del_usuario(db, conversation_id: int, owner_id: int):
    return (
        db.query(Conversation)
        .join(Assistant, Conversation.assistant_id == Assistant.id)
        .join(Project, Assistant.project_id == Project.id)
        .filter(Conversation.id == conversation_id, Project.owner_id == owner_id)
        .first()
    )


def crear_conversacion(assistant_id: int, owner_id: int, titulo: str):
    db = SessionLocal()
    try:
        if _asistente_del_usuario(db, assistant_id, owner_id) is None:
            return None

        conversacion = Conversation(assistant_id=assistant_id, titulo=titulo)
        db.add(conversacion)
        db.commit()
        db.refresh(conversacion)
        return conversacion
    finally:
        db.close()


def obtener_conversaciones(owner_id: int):
    db = SessionLocal()
    try:
        return (
            db.query(Conversation)
            .join(Assistant, Conversation.assistant_id == Assistant.id)
            .join(Project, Assistant.project_id == Project.id)
            .filter(Project.owner_id == owner_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )
    finally:
        db.close()


def obtener_conversacion(conversation_id: int, owner_id: int):
    db = SessionLocal()
    try:
        return _conversacion_del_usuario(db, conversation_id, owner_id)
    finally:
        db.close()


def crear_mensaje_usuario(conversation_id: int, owner_id: int, contenido: str):
    db = SessionLocal()
    try:
        conversacion = _conversacion_del_usuario(db, conversation_id, owner_id)
        if conversacion is None:
            return None

        mensaje = Message(
            conversation_id=conversation_id,
            role="user",
            contenido=contenido,
        )
        db.add(mensaje)
        conversacion.updated_at = db.func.now()
        db.commit()
        db.refresh(mensaje)
        return mensaje
    finally:
        db.close()


def obtener_mensajes(conversation_id: int, owner_id: int):
    db = SessionLocal()
    try:
        if _conversacion_del_usuario(db, conversation_id, owner_id) is None:
            return None

        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc(), Message.id.asc())
            .all()
        )
    finally:
        db.close()
