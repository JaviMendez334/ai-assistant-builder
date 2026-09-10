from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import backend.tools.registry

from backend.routers.home import router as home_router
from backend.routers.auth import router as auth_router
from backend.routers.profile import router as profile_router
from backend.routers.projects import router as projects_router
from backend.routers.assistants import router as assistants_router
from backend.routers.conversations import router as conversations_router
from backend.routers.documents import router as documents_router
from backend.routers.chat import router as chat_router


app = FastAPI(
    title="AI Assistant Builder API",
    version="1.0.0",
    description="Plataforma para crear asistentes IA empresariales con RAG y herramientas.",
)


# ==============================
# CORS CONFIG
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# ROUTERS
# ==============================

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(projects_router)
app.include_router(assistants_router)
app.include_router(conversations_router)
app.include_router(documents_router)
app.include_router(chat_router)
