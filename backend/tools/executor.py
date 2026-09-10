from typing import Any
from backend.tools.registry import registry
from backend.services.assistant_tool_service import (
    obtener_herramientas_asistente,
)


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
):
    """
    Ejecuta una herramienta registrada.
    """
    tool = registry.get(tool_name)

    if tool is None:
        return {
            "success": False,
            "message": f"La herramienta '{tool_name}' no existe.",
        }

    try:
        resultado = tool.execute(**arguments)
        return {
            "success": True,
            "tool": tool_name,
            "result": resultado,
        }
    except Exception as e:
        return {
            "success": False,
            "tool": tool_name,
            "message": str(e),
        }


def get_available_tools(assistant_id: int):
    """
    Devuelve las herramientas habilitadas para el asistente.
    Si no tiene ninguna vinculada en la base de datos, obtiene
    todas las herramientas registradas en el ToolRegistry.
    """
    nombres_herramientas = obtener_herramientas_asistente(assistant_id)

    # Si no hay herramientas asociadas explícitamente, obtener todas las registradas
    if not nombres_herramientas:
        tools_dict = getattr(registry, "_tools", getattr(registry, "tools", {}))
        return [tool.schema() for tool in tools_dict.values()]

    herramientas_disponibles = []
    for nombre in nombres_herramientas:
        herramienta = registry.get(nombre)
        if herramienta is not None:
            herramientas_disponibles.append(herramienta.schema())

    return herramientas_disponibles
