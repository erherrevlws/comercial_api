from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.detalle_venta import DetalleVenta, DetalleVentaCreate, DetalleVentaUpdate
from models.venta import Venta
from models.producto import Producto
from config.session_Dependencia import SessionDeDependencia

router = APIRouter()

@router.get("/detalle_ventas", response_model=list[DetalleVenta], status_code=status.HTTP_200_OK)
def get_detalles(
    session: SessionDeDependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1)
):
    consulta = select(DetalleVenta).offset(offset).limit(limit)
    return session.exec(consulta).all()

@router.get("/detalle_ventas/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
def get_detalle(id: int, session: SessionDeDependencia):
    detalle = session.exec(select(DetalleVenta).where(DetalleVenta.id == id)).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    return detalle

@router.post("/detalle_ventas", response_model=DetalleVenta, status_code=status.HTTP_201_CREATED)
def create_detalle(datos: DetalleVentaCreate, session: SessionDeDependencia):
    if not session.exec(select(Venta).where(Venta.id == datos.id_venta)).first():
        raise HTTPException(status_code=400, detail=f"Venta con ID {datos.id_venta} no existe")
    
    producto = session.exec(select(Producto).where(Producto.id == datos.id_producto)).first()
    if not producto:
        raise HTTPException(status_code=400, detail=f"Producto con ID {datos.id_producto} no existe")

    # Validar stock disponible
    if producto.stock < datos.cantidad:
        raise HTTPException(status_code=400, detail=f"Stock insuficiente. Disponible: {producto.stock}")

    # Descontar stock del producto
    producto.stock -= datos.cantidad
    session.add(producto)

    nuevo_detalle = DetalleVenta.model_validate(datos)
    session.add(nuevo_detalle)
    session.commit()
    session.refresh(nuevo_detalle)
    return nuevo_detalle

@router.delete("/detalle_ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_detalle(id: int, session: SessionDeDependencia):
    detalle = session.exec(select(DetalleVenta).where(DetalleVenta.id == id)).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    session.delete(detalle)
    session.commit()
    return None