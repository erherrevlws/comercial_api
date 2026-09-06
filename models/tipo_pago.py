from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class TipoPagoBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=255)

class TipoPago(TipoPagoBase, table=True):
    __tablename__ = "tipo_pago"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TipoPagoCreate(TipoPagoBase):
    pass

class TipoPagoUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=255)