from services.document_processor import extraer_texto_pdf
from services.chunking import dividir_en_chunks

texto = extraer_texto_pdf(
    "uploads/project_2/emprendimiento_moda_aura_co.pdf"
)

chunks = dividir_en_chunks(texto)

print(f"Total chunks: {len(chunks)}")

print(chunks[0])
