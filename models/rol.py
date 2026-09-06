from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class RolBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=255)

class Rol(RolBase, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RolCreate(RolBase):
    pass

class RolUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=255)