from backend.services.rag_service import generar_contexto
from backend.services.llm_service import generar_respuesta


pregunta = "¿Cuánto factura Aura & Co?"


contexto = generar_contexto(
    pregunta
)


respuesta = generar_respuesta(
    pregunta,
    contexto
)


print(respuesta)

