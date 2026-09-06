from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models import producto
from models.categoria import Categoria 
from models.producto import Producto, ProductoCreate, ProductoUpdate, ProductoUpdatePatch
from datetime import datetime

router = APIRouter()

@router.get("/productos", response_model=list[Producto], status_code=status.HTTP_200_OK)
def get_productos(
    session: SessionDeDependencia,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1)
):
    consulta = select(Producto).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
def get_producto(id: int, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return resultado_de_consulta

@router.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
def create_producto(datos_producto: ProductoCreate, session: SessionDeDependencia):

    consulta = select(Categoria).where(Categoria.id == datos_producto.id_categoria)
    categoria = session.exec(consulta).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría con id {datos_producto.id_categoria} no encontrada".format(datos_producto=datos_producto))

    nuevo_producto = Producto(
        nombre=datos_producto.nombre,
        descripcion=datos_producto.descripcion,
        precio_compra=datos_producto.precio_compra,
        precio_venta=datos_producto.precio_venta,
        stock=datos_producto.stock,
        imagen=datos_producto.imagen,
        categoria_id=datos_producto.categoria_id
    )
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)
    return nuevo_producto

@router.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(id: int, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    session.delete(resultado_de_consulta)
    session.commit()
    return None


@router.put("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
def update_producto(
    id: int,
    datos_producto: ProductoUpdate,
    session: SessionDeDependencia
):
    consulta = select(Producto).where(Producto.id == id)
    resultado_de_consulta = session.exec(consulta).first()

    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    categoria = session.exec(select(Categoria).where(Categoria.id == datos_producto.categoria_id)).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría con id {datos_producto.categoria_id} no encontrada, no se puede actualizar el producto")

    if datos_producto.descripcion:
        producto.descripcion = datos_producto.descripcion

    producto.nombre = datos_producto.nombre
    producto.precio_compra = datos_producto.precio_compra   
    producto.precio_venta = datos_producto.precio_venta
    producto.stock = datos_producto.stock
    producto.imagen = datos_producto.imagen
    producto.categoria_id = datos_producto.categoria_id
    producto.updated_at = datetime.utcnow()

    
    session.add(resultado_de_consulta)
    session.commit()
    session.refresh(resultado_de_consulta)
    return resultado_de_consulta

@router.patch("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
def patch_producto(id: int, datos_producto: ProductoUpdatePatch, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    if datos_producto.categoria_id:
        categoria = session.exec(select(Categoria).where(Categoria.id == datos_producto.categoria_id)).first()
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría con id {datos_producto.categoria_id} no encontrada, no se puede actualizar el producto")
        producto.categoria_id = datos_producto.categoria_id

    if datos_producto.nombre:
        producto.nombre = datos_producto.nombre

    if datos_producto.descripcion:
        producto.descripcion = datos_producto.descripcion

    if datos_producto.precio_compra:
        producto.precio_compra = datos_producto.precio_compra

    if datos_producto.precio_venta:
        producto.precio_venta = datos_producto.precio_venta

    if datos_producto.stock:
        producto.stock = datos_producto.stock

    if datos_producto.imagen:
        producto.imagen = datos_producto.imagen

    producto.updated_at = datetime.utcnow()
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto