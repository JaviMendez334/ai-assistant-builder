from groq import Groq

from backend.config.settings import settings


cliente = Groq(
    api_key=settings.GROQ_API_KEY,
)


modelos = cliente.models.list()

print("\n========== MODELOS DISPONIBLES ==========\n")

for modelo in modelos.data:
    print(modelo.id)
    