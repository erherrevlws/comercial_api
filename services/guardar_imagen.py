import os 
import shutil
import uuid
from fastapi import UploadFile, HTTPException, status

IMAGENES_DIRECCION = "imagenes"

def guardar_imagen(archivo: UploadFile) -> dict:
    if archivo.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de archivo no válido. Solo se permiten imágenes JPEG, PNG o WEBP."
        )

    os.makedirs(IMAGENES_DIRECCION, exist_ok=True)

    extension = os.path.splitext(archivo.filename)[1]
    nombre_archivo = f"{uuid.uuid4().hex}{extension}"
    ruta_destino = os.path.join(IMAGENES_DIRECCION, nombre_archivo)

    with open(ruta_destino, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    return {
        "nombre": nombre_archivo,
        "tipo": archivo.content_type,
        "url": f"/imagenes/{nombre_archivo}"
    }