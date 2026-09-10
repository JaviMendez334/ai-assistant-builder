from backend.services.search_service import buscar_chunks


def generar_contexto(pregunta: str):

    resultados = buscar_chunks(
        pregunta,
        limite=3
    )

    contexto = ""

    for resultado in resultados:
        contexto += resultado["chunk"]
        contexto += "\n\n"

    return contexto