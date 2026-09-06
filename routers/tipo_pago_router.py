from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.tipo_pago import TipoPago, TipoPagoCreate, TipoPagoUpdate
from config.session_Dependencia import SessionDeDependencia

router = APIRouter()

@router.get("/tipo_pago", response_model=list[TipoPago], status_code=status.HTTP_200_OK)
def get_tipos_pago(
    session: SessionDeDependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1)
):
    consulta = select(TipoPago).offset(offset).limit(limit)
    return session.exec(consulta).all()

@router.get("/tipo_pago/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
def get_tipo_pago(id: int, session: SessionDeDependencia):
    tipo = session.exec(select(TipoPago).where(TipoPago.id == id)).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    return tipo

@router.post("/tipo_pago", response_model=TipoPago, status_code=status.HTTP_201_CREATED)
def create_tipo_pago(datos: TipoPagoCreate, session: SessionDeDependencia):
    nuevo_tipo = TipoPago.model_validate(datos)
    session.add(nuevo_tipo)
    session.commit()
    session.refresh(nuevo_tipo)
    return nuevo_tipo

@router.patch("/tipo_pago/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
def update_tipo_pago(id: int, datos: TipoPagoUpdate, session: SessionDeDependencia):
    tipo = session.exec(select(TipoPago).where(TipoPago.id == id)).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    
    tipo.sqlmodel_update(datos.model_dump(exclude_unset=True))
    tipo.updated_at = datetime.utcnow()
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

@router.delete("/tipo_pago/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo_pago(id: int, session: SessionDeDependencia):
    tipo = session.exec(select(TipoPago).where(TipoPago.id == id)).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    session.delete(tipo)
    session.commit()
    return None