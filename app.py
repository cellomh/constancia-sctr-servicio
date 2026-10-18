"""
Servicio HTTP chico que genera la Constancia SCTR - Salud en PDF.

Qué hace:
  - Recibe un POST en /generar-constancia con los datos del asegurado (JSON).
  - Devuelve el PDF ya armado (bytes), usando el diseño aprobado por Cello
    (ver generar_constancia.py).
  - Pide un token secreto en el header "X-Service-Token" para que no
    cualquiera en internet pueda generar constancias. El valor del token
    se define en la variable de entorno SERVICE_TOKEN del servidor
    (Coolify), nunca en el código.

Pensado para correr dentro de Coolify (Hetzner), llamado por n8n
(flujo F2, nodo "10b") con un HTTP Request node.
"""

import os
import tempfile
import uuid

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from generar_constancia import generar_constancia

app = FastAPI(title="Constancia SCTR - Servicio de generación")

SERVICE_TOKEN = os.environ.get("SERVICE_TOKEN")


class Asegurado(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    numero_documento: str


class DatosConstancia(BaseModel):
    contrato_numero: str
    sede: str = "PRINCIPAL"
    empresa: str
    ruc: str
    vigencia_inicio: str
    vigencia_fin: str
    actividad: str
    asegurados: list[Asegurado] = Field(min_length=1)


@app.get("/salud")
def salud():
    """Endpoint simple para que Coolify confirme que el servicio está vivo."""
    return {"status": "ok"}


@app.post("/generar-constancia")
def generar(datos: DatosConstancia, x_service_token: str | None = Header(default=None)):
    if not SERVICE_TOKEN:
        raise HTTPException(status_code=500, detail="El servicio no tiene SERVICE_TOKEN configurado")
    if x_service_token != SERVICE_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

    datos_dict = datos.model_dump()
    nombre_archivo = f"constancia_{uuid.uuid4().hex}.pdf"
    ruta_salida = os.path.join(tempfile.gettempdir(), nombre_archivo)

    generar_constancia(datos_dict, ruta_salida)

    return FileResponse(
        ruta_salida,
        media_type="application/pdf",
        filename="constancia_sctr_salud.pdf",
    )
