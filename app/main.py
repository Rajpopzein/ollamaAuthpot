from fastapi import FastAPI
from app.routers.ollama_api import router as ollama_router
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(ollama_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Ollama FastAPI Service"}
