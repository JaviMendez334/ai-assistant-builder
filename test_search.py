from backend.services.search_service import buscar_chunks


resultado = buscar_chunks(
    "¿Cuánto factura anualmente Aura & Co?"
)


for r in resultado:
    print("----------------")
    print("Score:", r["score"])
    print(r["chunk"])


    