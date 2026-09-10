from backend.services.embedding_service import crear_embedding


texto = "Aura & Co tiene una facturación anual de 4.8 millones USD"

vector = crear_embedding(texto)

print(len(vector))
print(vector[:5])

