from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def extraer_texto_pdf(ruta: str) -> str:
    reader = PdfReader(ruta)

    texto = ""

    for pagina in reader.pages:
        contenido = pagina.extract_text()

        if contenido:
            texto += contenido + "\n"

    return texto


def crear_chunks(
    texto: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return splitter.split_text(texto)
