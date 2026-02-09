from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import (
    ModelAccessError,
    ollama_chat_service,
    ollama_stream_service,
)

router = APIRouter(prefix="/ollama", tags=["ollama"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_ollama(payload: ChatRequest, user: User = Depends(get_current_user)):
    try:
        response = ollama_chat_service(user=user, prompt=payload.prompt, model=payload.model)
        return ChatResponse(response=response)
    except ModelAccessError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

def stream_generator(response):
    for chunk in response:
        yield chunk["message"]["content"]

@router.post("/stream")
def stream_ollama_response(payload: ChatRequest, user: User = Depends(get_current_user)):
    try:
        response = ollama_stream_service(user=user, prompt=payload.prompt, model=payload.model)
        return StreamingResponse(stream_generator(response), media_type="text/event-stream")
    except ModelAccessError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
