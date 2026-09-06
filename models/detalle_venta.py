from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field

class DetalleVentaBase(SQLModel):
    id_venta: int = Field(nullable=False, foreign_key="ventas.id")
    id_producto: int = Field(nullable=False, foreign_key="productos.id")
    cantidad: int = Field(nullable=False, gt=0)
    precio_unitario: Decimal = Field(nullable=False, gt=0)
    subtotal: Decimal = Field(nullable=False, ge=0)

class DetalleVenta(DetalleVentaBase, table=True):
    __tablename__ = "detalle_ventas"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaUpdate(SQLModel):
    id_venta: Optional[int] = Field(default=None)
    id_producto: Optional[int] = Field(default=None)
    cantidad: Optional[int] = Field(default=None, gt=0)
    precio_unitario: Optional[Decimal] = Field(default=None, gt=0)
    subtotal: Optional[Decimal] = Field(default=None, ge=0)