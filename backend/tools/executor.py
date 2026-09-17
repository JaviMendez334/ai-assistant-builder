import inspect
from typing import Any
from backend.tools.registry import registry
from backend.services.assistant_tool_service import obtener_herramientas_asistente


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """
    Ejecuta una herramienta registrada de forma sincrónica.
    """
    tool = registry.get(tool_name)

    if tool is None:
        return {
            "success": False,
            "tool": tool_name,
            "message": f"La herramienta '{tool_name}' no está registrada en el sistema.",
        }

    try:
        resultado = tool.execute(**arguments)

        return {
            "success": True,
            "tool": tool_name,
            "result": resultado,
        }
    except TypeError as e:
        return {
            "success": False,
            "tool": tool_name,
            "message": f"Argumentos inválidos para '{tool_name}': {e}",
        }
    except Exception as e:
        return {
            "success": False,
            "tool": tool_name,
            "message": f"Error en la ejecución: {str(e)}",
        }


def get_available_tools(assistant_id: int) -> list[dict[str, Any]]:
    """
    Devuelve los esquemas de las herramientas habilitadas para el asistente.
    """
    nombres_herramientas = obtener_herramientas_asistente(assistant_id)

    if not nombres_herramientas:
        if hasattr(registry, "get_all"):
            todas = registry.get_all()
        else:
            todas = getattr(registry, "_tools", getattr(registry, "tools", {})).values()
        return [tool.schema() for tool in todas]

    herramientas_disponibles = []
    for nombre in nombres_herramientas:
        herramienta = registry.get(nombre)
        if herramienta is not None:
            herramientas_disponibles.append(herramienta.schema())

    return herramientas_disponibles
