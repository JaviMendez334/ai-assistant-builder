import json

from backend.tools.executor import execute_tool
from backend.tools.executor import registry


def obtener_tools():

    return registry.schemas()


def ejecutar_tool_call(tool_call):

    nombre = tool_call.function.name

    argumentos = json.loads(
        tool_call.function.arguments
    )

    resultado = execute_tool(
        nombre,
        argumentos,
    )

    return {
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": nombre,
        "content": json.dumps(
            resultado,
            ensure_ascii=False,
        ),
    }
