from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class ClienteBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100)
    apellido: str = Field(nullable=False, max_length=100)
    telefono: str = Field(nullable=False, min_length=9, max_length=9)  # Exactamente 9 dígitos
    correo: Optional[str] = Field(default=None, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=255)

class Cliente(ClienteBase, table=True):
    __tablename__ = "clientes"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=100)
    apellido: Optional[str] = Field(default=None, max_length=100)
    telefono: Optional[str] = Field(default=None, min_length=9, max_length=9)
    correo: Optional[str] = Field(default=None, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=255)