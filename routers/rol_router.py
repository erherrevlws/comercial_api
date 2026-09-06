from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.rol import Rol, RolCreate, RolUpdate
from config.session_Dependencia import SessionDeDependencia
from typing import Optional
from sqlmodel import select
from fastapi import APIRouter, HTTPException, status, Query

router = APIRouter()

@router.get("/roles", response_model=list[Rol], status_code=status.HTTP_200_OK)
def get_roles(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    return session.exec(select(Rol).offset(offset).limit(limit)).all()

@router.post("/roles", response_model=Rol, status_code=status.HTTP_201_CREATED)
def create_rol(datos: RolCreate, session: SessionDeDependencia):
    nuevo_rol = Rol.model_validate(datos)
    session.add(nuevo_rol)
    session.commit()
    session.refresh(nuevo_rol)
    return nuevo_rol

@router.patch("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
def update_rol(id: int, datos: RolUpdate, session: SessionDeDependencia):
    rol = session.exec(select(Rol).where(Rol.id == id)).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    rol.sqlmodel_update(datos.model_dump(exclude_unset=True))
    rol.updated_at = datetime.utcnow()
    session.add(rol)
    session.commit()
    session.refresh(rol)
    return rol

@router.delete("/roles/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rol(id: int, session: SessionDeDependencia):
    rol = session.exec(select(Rol).where(Rol.id == id)).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    session.delete(rol)
    session.commit()
    return None