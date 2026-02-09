from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    models = relationship("Model", secondary="user_models", back_populates="users")

class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    users = relationship("User", secondary="user_models", back_populates="models")

user_models = Table(
    "user_models",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("model_id", Integer, ForeignKey("models.id")),
)
