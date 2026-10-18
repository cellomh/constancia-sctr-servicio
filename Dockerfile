FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema que reportlab necesita para fuentes/imagenes
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py generar_constancia.py ./
COPY logo_sanitas.png firma_sanitas.png qr_ejemplo.png ./

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
