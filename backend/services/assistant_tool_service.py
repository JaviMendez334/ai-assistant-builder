from backend.database.session import SessionLocal
from backend.models.assistant_tool import AssistantTool


def obtener_herramientas_asistente(
    assistant_id: int,
):
    db = SessionLocal()

    try:
        herramientas = (
            db.query(AssistantTool.tool_name)
            .filter(
                AssistantTool.assistant_id == assistant_id,
                AssistantTool.activo == True,
            )
            .all()
        )

        return [
            herramienta.tool_name
            for herramienta in herramientas
        ]

    finally:
        db.close()
        