from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.rol import Rol, RolCreate, RolUpdate
from config.session_Dependencia import SessionDeDependencia
from typing import Optional
from sqlmodel import select
from fastapi import APIRouter, HTTPException, status, Query
from config.session_Dependencia import SessionDeDependencia
from config.security_Dependencia import Token_Dependencia

router = APIRouter()

@router.get("/roles", response_model=list[Rol], status_code=status.HTTP_200_OK)
def get_roles(
    session: SessionDeDependencia,
    token : Token_Dependencia,
      offset: int = Query(0, ge=0), 
      limit: int = Query(20, ge=1)
      ):
    if token["id_rol"] != 1:
        raise HTTPException(status_code=403, detail="Solo el administrador puede consultar roles")
    return session.exec(select(Rol).offset(offset).limit(limit)).all()


@router.get("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
def get_rol(
    id: int,
      session: SessionDeDependencia,
      token: Token_Dependencia
      ):
    if token["id_rol"] != 1:
        raise HTTPException(status_code=403, detail="Solo el administrador puede consultar los roles")
    consulta = select(Rol).where(
        Rol.id == id
    )

    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta: 
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return resultado_de_consulta

@router.post("/roles", response_model=Rol, status_code=status.HTTP_201_CREATED)
def create_rol(
    datos: RolCreate,
    token: Token_Dependencia,
    session: SessionDeDependencia
    ):
    if token["id_rol"] != 1:
        raise HTTPException(status_code=403, detail="Solo el administrador puede crear roles")
    nuevo_rol = Rol.model_validate(datos)
    session.add(nuevo_rol)
    session.commit()
    session.refresh(nuevo_rol)
    return nuevo_rol



@router.delete("/roles/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rol(
    id: int, 
    token: Token_Dependencia,
    session: SessionDeDependencia
    ):
    if token["id_rol"] != 1:
        raise HTTPException(status_code=403, detail="Solo el administrador puede eliminar roles")
    rol = session.exec(select(Rol).where(Rol.id == id)).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    session.delete(rol)
    session.commit()
    return None

@router.put("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
def update_rol(
    id: int,
      datos_rol: RolUpdate,
        session: SessionDeDependencia,
        token: Token_Dependencia
        ):
    if token["id_rol"] != 1:
        raise HTTPException(status_code=403, detail="Solo el administrador puede actualizar roles")
    consulta = select(Rol).where(Rol.id == id)
    resultado_de_consulta = session.exec(consulta).first()

    if not resultado_de_consulta:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    resultado_de_consulta.nombre = datos_rol.nombre = datos_rol.descripcion

    session.add(resultado_de_consulta)

    session.commit()
    session.refresh(resultado_de_consulta)
    return resultado_de_consulta