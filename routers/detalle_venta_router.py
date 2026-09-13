from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.detalle_venta import DetalleVenta, DetalleVentaCreate, DetalleVentaUpdate
from models.venta import Venta
from models.producto import Producto
from config.session_Dependencia import SessionDeDependencia
from config.security_Dependencia import Token_Dependencia

router = APIRouter()

@router.get("/detalle_ventas", response_model=list[DetalleVenta], status_code=status.HTTP_200_OK)
def get_detalles(
    session: SessionDeDependencia,
    token: Token_Dependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1)
):

    if token["id_rol"] == 1:
        consulta = select(DetalleVenta).offset(offset).limit(limit)
        return session.exec(consulta).all()
    
    consulta = select(DetalleVenta).offset(offset).limit(limit)
    return session.exec(consulta).all()

@router.get("/detalle_ventas/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
def get_detalle(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    detalle = session.exec(select(DetalleVenta).where(DetalleVenta.id == id)).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")

    if token["id_rol"] != 1:
        venta = session.exec(select(Venta).where(Venta.id == detalle.id_venta)).first()
        if not venta or venta.id_usuario != token["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes consultar detalles de tus propias ventas"
            )
    return detalle

@router.post("/detalle_ventas", response_model=DetalleVenta, status_code=status.HTTP_201_CREATED)
def create_detalle(
    datos: DetalleVentaCreate,
    session: SessionDeDependencia,
    token: Token_Dependencia
):
    venta = session.exec(select(Venta).where(Venta.id == datos.id_venta)).first()
    if not venta:
        raise HTTPException(status_code=400, detail=f"Venta con ID {datos.id_venta} no existe")

    if token["id_rol"] != 1 and venta.id_usuario != token["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes registrar detalles en tus propias ventas"
        )

    producto = session.exec(select(Producto).where(Producto.id == datos.id_producto)).first()
    if not producto:
        raise HTTPException(status_code=400, detail=f"Producto con ID {datos.id_producto} no existe")

    if producto.stock < datos.cantidad:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente. Disponible: {producto.stock}"
        )

    # Descontar stock del producto
    producto.stock -= datos.cantidad
    session.add(producto)

    nuevo_detalle = DetalleVenta.model_validate(datos)
    session.add(nuevo_detalle)
    session.commit()
    session.refresh(nuevo_detalle)
    return nuevo_detalle

@router.patch("/detalle_ventas/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
def update_detalle(
    id: int,
    datos: DetalleVentaUpdate,
    session: SessionDeDependencia,
    token: Token_Dependencia
):
    detalle = session.exec(select(DetalleVenta).where(DetalleVenta.id == id)).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")

    venta = session.exec(select(Venta).where(Venta.id == detalle.id_venta)).first()
    if token["id_rol"] != 1 and (not venta or venta.id_usuario != token["id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes modificar detalles de tus propias ventas"
        )

    # Si se actualiza la cantidad ajustar el stock 
    if datos.cantidad is not None and datos.cantidad != detalle.cantidad:
        producto = session.exec(select(Producto).where(Producto.id == detalle.id_producto)).first()
        diferencia = datos.cantidad - detalle.cantidad
        if producto.stock < diferencia:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para el cambio. Disponible: {producto.stock}"
            )
        producto.stock -= diferencia
        session.add(producto)

    detalle.sqlmodel_update(datos.model_dump(exclude_unset=True))
    detalle.updated_at = datetime.utcnow()
    session.add(detalle)
    session.commit()
    session.refresh(detalle)
    return detalle

@router.delete("/detalle_ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_detalle(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    detalle = session.exec(select(DetalleVenta).where(DetalleVenta.id == id)).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")

    venta = session.exec(select(Venta).where(Venta.id == detalle.id_venta)).first()
    if token["id_rol"] != 1 and (not venta or venta.id_usuario != token["id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes eliminar detalles de tus propias ventas"
        )

    # Restaurar existencias al inventario antes de eliminar el registro
    producto = session.exec(select(Producto).where(Producto.id == detalle.id_producto)).first()
    if producto:
        producto.stock += detalle.cantidad
        session.add(producto)

    session.delete(detalle)
    session.commit()
    return None