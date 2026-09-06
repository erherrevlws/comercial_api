from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class UsuarioBase(SQLModel):
    username: str = Field(nullable=False, max_length=50, unique=True)  # Username único
    nombre: str = Field(nullable=False, max_length=100)
    apellido: str = Field(nullable=False, max_length=100)
    telefono: str = Field(nullable=False, min_length=9, max_length=9)
    correo: Optional[str] = Field(default=None, max_length=150)
    id_rol: int = Field(nullable=False, foreign_key="roles.id")

class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UsuarioCreate(UsuarioBase):
    password: str = Field(nullable=False, min_length=6, max_length=255)

class UsuarioUpdate(SQLModel):
    username: Optional[str] = Field(default=None, max_length=50)
    nombre: Optional[str] = Field(default=None, max_length=100)
    apellido: Optional[str] = Field(default=None, max_length=100)
    telefono: Optional[str] = Field(default=None, min_length=9, max_length=9)
    correo: Optional[str] = Field(default=None, max_length=150)
    id_rol: Optional[int] = Field(default=None)
    password: Optional[str] = Field(default=None, min_length=6, max_length=255)