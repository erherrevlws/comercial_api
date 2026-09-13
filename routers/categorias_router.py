from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.categoria import Categoria, CategoriaCreate, CategoriaUpdate
from config.session_Dependencia import SessionDeDependencia
# En routers/categorias_router.py
from config.security_Dependencia import Token_Dependencia

router = APIRouter()

@router.get("/categorias", response_model=list[Categoria], status_code=status.HTTP_200_OK)
async def get_categorias(
    session: SessionDeDependencia,
    token: Token_Dependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1)
):
    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para acceder a esta informacion")


    consulta = select(Categoria).offset(offset).limit(limit)
    resultado = session.exec(consulta)
    return resultado.all()

@router.get("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def get_categoria(session: SessionDeDependencia,
                        token: Token_Dependencia,
                        offset: int = Query(0, ge=0),
                        limit: int = Query(20, ge=1)):
    consulta = select(Categoria).offset(offset).limit(
        limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()

@router.post("/categorias", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def create_categoria(
    datos_categoria: CategoriaCreate, 
    session: SessionDeDependencia, 
    token: Token_Dependencia
    ):

    if token["id_rol"] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Solo el administrador puede crear categorias")
    nueva_categoria = Categoria(
        nombre=datos_categoria.nombre,
        descripcion=datos_categoria.descripcion
    )
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria

@router.delete("/categorias/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    if token['id_rol'] != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Solo el adminsitrador puede eliminar categorias")
    consulta = select(Categoria).where(Categoria.id == id)
    categoria = session.exec(consulta).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    session.delete(categoria)
    session.commit()
    return None

@router.put("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def update_categoria(
    id: int,
    datos_categoria: CategoriaUpdate,
    session: SessionDeDependencia,
    token: Token_Dependencia
):
    if token['id_rol'] != 1:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Solo el adminsitrador puede modificar categorias")
    resultado_de_consulta = select(Categoria).where(Categoria.id == id)
    categoria = session.exec(consulta).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    resultado_de_consulta.nombre = datos_categoria.nombre
    if datos_categoria.descripcion is not None:
        resultado_de_consulta.descripcion = datos_categoria.descripcion
    
    resultado_de_consulta.updated_at = datetime.utcnow()
    
    session.add(resultado_de_consulta)
    session.commit()
    session.refresh(resultado_de_consulta)
    return resultado_de_consulta