from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.database import Base

user_models = Table(
    "user_models",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("model_id", Integer, ForeignKey("models.id")),
)
