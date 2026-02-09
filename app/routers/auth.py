from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.routers.deps import get_db
from app.schemas.schemas import APIKeyRequest, APIKeyResponse
from app.services.auth_service import generate_api_key_for_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/generate-key", response_model=APIKeyResponse)
def generate_api_key(payload: APIKeyRequest, db: Session = Depends(get_db)):
    api_key = generate_api_key_for_user(db, payload.username)
    return APIKeyResponse(api_key=api_key)
