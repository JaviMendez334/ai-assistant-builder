from groq import Groq

from backend.config.settings import settings


cliente = Groq(
    api_key=settings.GROQ_API_KEY,
)


def rerank_chunks(
    pregunta: str,
    chunks: list[dict],
):
    """
    Reordena los chunks según su relevancia usando Groq.
    """

    if len(chunks) <= 1:
        return chunks

    texto_chunks = ""

    for i, chunk in enumerate(chunks):

        texto_chunks += f"""

CHUNK {i + 1}

{chunk["chunk"]}

------------------------
"""

    prompt = f"""
Eres un experto en recuperación de información (RAG).

Debes ordenar los siguientes fragmentos desde el MÁS útil hasta el MENOS útil para responder la pregunta.

Pregunta:

{pregunta}

Fragmentos:

{texto_chunks}

Responde ÚNICAMENTE con los números separados por comas.

Ejemplo:

3,1,2,4

No expliques nada.
"""

    respuesta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    orden = respuesta.choices[0].message.content.strip()

    try:

        indices = [
            int(x.strip()) - 1
            for x in orden.split(",")
        ]

        nuevos_chunks = []

        for indice in indices:

            if 0 <= indice < len(chunks):
                nuevos_chunks.append(chunks[indice])

        return nuevos_chunks

    except Exception:

        return chunks
    