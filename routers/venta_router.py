from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.venta import Venta, VentaCreate, VentaUpdate
from models.cliente import Cliente
from models.usuario import Usuario
from models.tipo_pago import TipoPago
from config.session_Dependencia import SessionDeDependencia
from config.security_Dependencia import Token_Dependencia


router = APIRouter()

@router.get("/ventas", response_model=list[Venta], status_code=status.HTTP_200_OK)
def get_ventas(
    session: SessionDeDependencia,
    token: Token_Dependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1)
):
    
    consulta = select(Venta).offset(offset).limit(limit)
    if token["id_rol"] != 1:
        consulta = consulta.where(Venta.id_usuario == token["id"])
    return session.exec(consulta).all()

@router.get("/ventas/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
def get_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    venta = session.exec(select(Venta).where(Venta.id == id)).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    if token["id_rol"] != 1 and venta.id_usuario != token["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Solo puedes consultar tus propias ventas"
        )
    return venta

@router.post("/ventas", response_model=Venta, status_code=status.HTTP_201_CREATED)
def create_venta(datos: VentaCreate, session: SessionDeDependencia, token: Token_Dependencia):
    datos.id_usuario = token["id"]  
      # Validacion de llaves foraneas
    if not session.exec(select(Cliente).where(Cliente.id == datos.id_cliente)).first():
        raise HTTPException(status_code=400, detail=f"Cliente {datos.id_cliente} no existe")
    if not session.exec(select(Usuario).where(Usuario.id == datos.id_usuario)).first():
        raise HTTPException(status_code=400, detail=f"Usuario {datos.id_usuario} no existe")
    if not session.exec(select(TipoPago).where(TipoPago.id == datos.id_tipo_pago)).first():
        raise HTTPException(status_code=400, detail=f"Tipo de pago {datos.id_tipo_pago} no existe")

    nueva_venta = Venta.model_validate(datos)
    session.add(nueva_venta)
    session.commit()
    session.refresh(nueva_venta)
    return nueva_venta

@router.patch("/ventas/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
def update_venta(id: int, datos: VentaUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    venta = session.exec(select(Venta).where(Venta.id == id)).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    if token["id_rol"] != 1:
        if venta.id_usuario != token["id"]:
            raise HTTPException(status_code=403, detail="No puedes modificar una venta ajena")
        if datos.id_usuario is not None and datos.id_usuario != token["id"]:
            raise HTTPException(status_code=403, detail="No puedes reasignar la venta a otro usuario")

    if datos.id_cliente and not session.exec(select(Cliente).where(Cliente.id == datos.id_cliente)).first():
        raise HTTPException(status_code=400, detail=f"Cliente {datos.id_cliente} no existe")
    if datos.id_usuario and not session.exec(select(Usuario).where(Usuario.id == datos.id_usuario)).first():
        raise HTTPException(status_code=400, detail=f"Usuario {datos.id_usuario} no existe")
    if datos.id_tipo_pago and not session.exec(select(TipoPago).where(TipoPago.id == datos.id_tipo_pago)).first():
        raise HTTPException(status_code=400, detail=f"Tipo de pago {datos.id_tipo_pago} no existe")

    venta.sqlmodel_update(datos.model_dump(exclude_unset=True))
    venta.updated_at = datetime.utcnow()
    session.add(venta)
    session.commit()
    session.refresh(venta)
    return venta

@router.delete("/ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    if token["id_rol"] != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Solo el administrador puede anular o eliminar ventas"
        )
    venta = session.exec(select(Venta).where(Venta.id == id)).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    session.delete(venta)
    session.commit()
    return None