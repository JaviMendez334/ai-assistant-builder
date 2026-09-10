from backend.services.rag_service import generar_contexto


contexto = generar_contexto(
    "¿Cuánto factura anualmente Aura & Co?"
)


print("====================")
print(contexto)
print("====================")
