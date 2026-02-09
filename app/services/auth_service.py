from __future__ import annotations

import hashlib
import os
import secrets
from typing import Optional

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from app.models.apikey import APIKey
from app.models.user import User

_fernet_key = os.getenv("FERNET_KEY")
if _fernet_key is None:
    _fernet_key = Fernet.generate_key()
else:
    _fernet_key = _fernet_key.encode()

fernet = Fernet(_fernet_key)

def _hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()

def _get_or_create_user(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    user = User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def generate_api_key_for_user(db: Session, username: str) -> str:
    user = _get_or_create_user(db, username)
    raw_key = secrets.token_urlsafe(32)
    encrypted_key = fernet.encrypt(raw_key.encode()).decode()
    key_hash = _hash_key(raw_key)
    api_key = APIKey(encrypted_key=encrypted_key, key_hash=key_hash, user_id=user.id)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return raw_key

def verify_api_key(db: Session, raw_key: str) -> Optional[User]:
    key_hash = _hash_key(raw_key)
    api_key = db.query(APIKey).filter(APIKey.key_hash == key_hash).first()
    if not api_key:
        return None
    return api_key.user
