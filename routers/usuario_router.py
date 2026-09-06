from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from models.rol import Rol
from config.session_Dependencia import SessionDeDependencia
from typing import Optional
from sqlmodel import select
from fastapi import APIRouter, HTTPException, status, Query
router = APIRouter()

@router.get("/usuarios", response_model=list[Usuario], status_code=status.HTTP_200_OK)
def get_usuarios(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    return session.exec(select(Usuario).offset(offset).limit(limit)).all()

@router.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def create_usuario(datos: UsuarioCreate, session: SessionDeDependencia):
    if not session.exec(select(Rol).where(Rol.id == datos.id_rol)).first():
        raise HTTPException(status_code=400, detail=f"El rol con ID {datos.id_rol} no existe")
    
    if session.exec(select(Usuario).where(Usuario.username == datos.username)).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")

    nuevo_usuario = Usuario.model_validate(datos)
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return nuevo_usuario

@router.patch("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
def update_usuario(id: int, datos: UsuarioUpdate, session: SessionDeDependencia):
    usuario = session.exec(select(Usuario).where(Usuario.id == id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.id_rol and not session.exec(select(Rol).where(Rol.id == datos.id_rol)).first():
        raise HTTPException(status_code=400, detail=f"El rol con ID {datos.id_rol} no existe")

    if datos.username:
        existente = session.exec(select(Usuario).where(Usuario.username == datos.username)).first()
        if existente and existente.id != id:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    usuario.sqlmodel_update(datos.model_dump(exclude_unset=True))
    usuario.updated_at = datetime.utcnow()
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(id: int, session: SessionDeDependencia):
    usuario = session.exec(select(Usuario).where(Usuario.id == id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return None