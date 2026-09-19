from fastapi import FastAPI, status
from contextlib import asynccontextmanager  
from config.db import crear_db_y_tablas
from routers.categorias_router import router as categorias_router
from routers.producto_router import router as producto_router
from routers.rol_router import router as roles_router
from routers.usuario_router import router as usuarios_router
from routers.tipo_pago_router import router as tipo_pago_router
from routers.cliente_router import router as clientes_router
from routers.venta_router import router as ventas_router
from routers.detalle_venta_router import router as detalle_ventas_router  
from oauth.oauth import router as oauth_router  
import models as models
import os
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield

app = FastAPI(lifespan=lifespan)
app.title = "API Tienda la Cachacha"
app.version = "0.0.1"

#codigo implementado para la carga de imagenes
os.makedirs("imagenes", exist_ok=True)
app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")

@app.get("/", summary="Comprobando esta de api", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "ok"}

app.include_router(categorias_router, tags=["Categorias"])
app.include_router(producto_router, tags=["Productos"])
app.include_router(roles_router, tags=["roles"])
app.include_router(usuarios_router, tags=["usuarios"])
app.include_router(tipo_pago_router, tags=["tipo_pago"])
app.include_router(clientes_router, tags=["clientes"])
app.include_router(ventas_router, tags=["ventas"])
app.include_router(detalle_ventas_router, tags=["detalle_ventas"])
app.include_router(oauth_router, tags=["oauth"])

