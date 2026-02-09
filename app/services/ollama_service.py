from __future__ import annotations

import ollama

from app.models.user import User

class ModelAccessError(Exception):
    """Raised when a user attempts to access a model they do not own."""

def _ensure_model_access(user: User, model_name: str) -> None:
    if not any(m.name == model_name for m in user.models):
        raise ModelAccessError(f"User does not have access to model '{model_name}'")

def ollama_chat_service(user: User, prompt: str, model: str):
    _ensure_model_access(user, model)
    return ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

def ollama_stream_service(user: User, prompt: str, model: str):
    _ensure_model_access(user, model)
    return ollama.chat(model=model, messages=[{"role": "user", "content": prompt}], stream=True)
