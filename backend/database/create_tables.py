from backend.database.database import engine
from backend.models.user import Base

from backend.models.assistant import Assistant
from backend.models.assistant_tool import AssistantTool

Base.metadata.create_all(bind=engine)

print("✅ Tablas creadas correctamente")
