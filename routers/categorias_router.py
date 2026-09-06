from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from models.categoria import Categoria, CategoriaCreate, CategoriaUpdate
from config.session_Dependencia import SessionDeDependencia

router = APIRouter()

@router.get("/categorias", response_model=list[Categoria], status_code=status.HTTP_200_OK)
async def get_categorias(
    session: SessionDeDependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1)
):
    consulta = select(Categoria).offset(offset).limit(limit)
    resultado = session.exec(consulta)
    return resultado.all()

@router.get("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def get_categoria(id: int, session: SessionDeDependencia):
    consulta = select(Categoria).where(Categoria.id == id)
    categoria = session.exec(consulta).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

@router.post("/categorias", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def create_categoria(datos_categoria: CategoriaCreate, session: SessionDeDependencia):
    nueva_categoria = Categoria(
        nombre=datos_categoria.nombre,
        descripcion=datos_categoria.descripcion
    )
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria

@router.delete("/categorias/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(id: int, session: SessionDeDependencia):
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
    session: SessionDeDependencia
):
    consulta = select(Categoria).where(Categoria.id == id)
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