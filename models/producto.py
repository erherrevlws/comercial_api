from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ProductoBase(SQLModel):
    nombre: str = Field(nullable=False, min_length=4, max_length=255)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    precio_compra: Decimal = Field(nullable=False, gt=0)
    precio_venta: Decimal = Field(nullable=False, gt=0)
    stock: int = Field(nullable=False, ge=0)
    imagen: str = Field(nullable=False, max_length=255)
    categoria_id: int = Field(nullable=False, foreign_key="categorias.id")

class Producto(ProductoBase, table=True):
    __tablename__ = "productos"
    
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class ProductoUpdatePatch(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=4, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    precio_compra: Optional[Decimal] = Field(default=None, gt=0)
    precio_venta: Optional[Decimal] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    imagen: Optional[str] = Field(default=None, max_length=255)
    categoria_id: Optional[int] = Field(default=None)
