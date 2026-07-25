def dividir_en_chunks(
    texto: str,
    chunk_size: int = 800,
    overlap: int = 150,
):
    chunks = []

    inicio = 0

    while inicio < len(texto):
        fin = inicio + chunk_size

        chunks.append(texto[inicio:fin])

        inicio += chunk_size - overlap

    return chunks
