from groq import Groq
from backend.config.settings import settings

cliente = Groq(
    api_key=settings.GROQ_API_KEY,
)

def generar_respuesta(
    messages: list,
    tools: list | None = None,
    tool_choice="auto",
    temperature: float = 0,
):
    parametros = {
        "model": settings.GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    # Solo enviar tools si la lista existe Y contiene elementos
    if tools and len(tools) > 0:
        parametros["tools"] = tools
        parametros["tool_choice"] = tool_choice

    respuesta = cliente.chat.completions.create(
        **parametros
    )

    return respuesta


def generar_respuesta_stream(
    messages: list,
    temperature: float = 0,
):
    """
    Generador para streaming de tokens en tiempo real.
    """
    response = cliente.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        temperature=temperature,
        stream=True,
    )
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content
            