from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.auth_service import verify_api_key

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(x_api_key: str = Header(..., alias="X-API-Key"), db: Session = Depends(get_db)):
    user = verify_api_key(db, x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return user
