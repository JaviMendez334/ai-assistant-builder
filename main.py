from fastapi import FastAPI
from routers.home import router as home_router
from routers.auth import router as auth_router
from routers.profile import router as profile_router
from routers.projects import router as projects_router
from routers.assistants import router as assistants_router
from routers.conversations import router as conversations_router
from routers.documents import router as documents_router



app = FastAPI(
    title="AI Assistant Builder API"
)


app.include_router(home_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(projects_router)
app.include_router(assistants_router)
app.include_router(conversations_router)
app.include_router(documents_router)

