from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.session_Dependencia import SessionDeDependencia
from lib.pwd import get_password_hash
from models.rol import Rol
from config.session_Dependencia import SessionDeDependencia
from config.security_Dependencia import Token_Dependencia
from models.usuario import (
    Usuario,
    UsuarioCreate,
    UsuarioUpdate,
)

router = APIRouter()


@router.get(
    "/usuarios",
    response_model=list[Usuario],
    status_code=status.HTTP_200_OK
)
async def get_usuarios(
    session: SessionDeDependencia,
    token: Token_Dependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    if token["id_rol"] != 1:
        return session.exec(select(Usuario).where(Usuario.id == token["id"])).all()
    return session.exec(select(Usuario).offset(offset).limit(limit)).all()
    
    


@router.get(
    "/usuarios/{id}",
    response_model=Usuario,
    status_code=status.HTTP_200_OK
)
async def get_usuario(
    id: int,
    session: SessionDeDependencia,
    token: Token_Dependencia
):
    if token["id_rol"] != 1 and id != token["id"]:
        raise HTTPException(status_code=403, detail="Solo puedes consultar tu propio usuario")
    
    usuario = session.exec(
        select(Usuario).where(Usuario.id == id)
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post(
    "/usuarios",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED
)
async def create_usuario(
    datos: UsuarioCreate,
    session: SessionDeDependencia,
    token: Token_Dependencia
):
    if token["id_rol"] != 1:
        raise HTTPException(status_code=403, detail="Solo el administrador puede registrar nuevos usuarios")
    
    rol = session.exec(
        select(Rol).where(Rol.id == datos.id_rol)
    ).first()

    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El rol con ID {datos.id_rol} no existe"
        )

    usuario_existente = session.exec(
        select(Usuario).where(
            Usuario.username == datos.username
        )
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El nombre de usuario ya está registrado"
        )

    datos_diccionario = datos.model_dump()
    datos_diccionario["password"] = get_password_hash(datos_diccionario["password"])
    nuevo_usuario = Usuario.model_validate(datos_diccionario)

    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    return nuevo_usuario


@router.patch(
    "/usuarios/{id}",
    response_model=Usuario,
    status_code=status.HTTP_200_OK
)
async def patch_usuario(
    id: int,
    datos_usuario: UsuarioUpdate,
    session: SessionDeDependencia,
    token: Token_Dependencia
):
    if token["id_rol"] !=1:
        if id != token["id"]:
            raise HTTPException(status_code=403, detail="Solo puedes modificar tu propia cuenta")
        if datos_usuario.id_rol is not None:
            raise HTTPException(status_code=403, detail="No tienes permisos para cambiar tu rol")
    usuario = session.exec(
        select(Usuario).where(Usuario.id == id)
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    datos = datos_usuario.model_dump(exclude_unset=True)

    if "username" in datos:
        usuario_existente = session.exec(
            select(Usuario).where(
                Usuario.username == datos["username"],
                Usuario.id != id
            )
        ).first()

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El nombre de usuario ya está registrado"
            )

    if "id_rol" in datos:
        rol = session.exec(
            select(Rol).where(
                Rol.id == datos["id_rol"]
            )
        ).first()

        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )

        if "password" in datos and datos["password"]:
            datos["password"] = get_password_hash(datos["password"])

    usuario.sqlmodel_update(datos)

    usuario.updated_at = datetime.now(timezone.utc)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.delete(
    "/usuarios/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_usuario(
    id: int,
    session: SessionDeDependencia,
    token: Token_Dependencia
):
    if token["id_rol"] != 1:
        raise HTTPException(status_code=403, detail="Solo el administrador puede eliminar usuarios")
    usuario = session.exec(
        select(Usuario).where(Usuario.id == id)
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    session.delete(usuario)
    session.commit()

    return None
