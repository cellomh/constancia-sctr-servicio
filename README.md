# Servicio: Generar Constancia SCTR - Salud (PDF)

Servicio chico en Python (FastAPI) que genera la constancia SCTR en PDF.
Pensado para correr en Coolify (servidor Hetzner de Viscaya) y ser llamado
por n8n desde el flujo F2, nodo "10b".

## Endpoints

- `GET /salud` → `{"status":"ok"}` (para que Coolify verifique que está vivo)
- `POST /generar-constancia` → recibe los datos del asegurado en JSON y
  devuelve el PDF. Requiere el header `X-Service-Token` con el valor
  configurado en la variable de entorno `SERVICE_TOKEN`.

## Variable de entorno requerida

- `SERVICE_TOKEN`: una clave secreta cualquiera que tú elijas, para que
  solo n8n pueda pedir constancias. Se configura en Coolify al crear la
  aplicación, y el mismo valor se usa en el credential de n8n que llama
  a este servicio.

## Despliegue en Coolify

1. Subir esta carpeta a un repositorio de GitHub.
2. En Coolify: Nueva aplicación → origen = ese repositorio → tipo de build =
   Dockerfile (Coolify lo detecta solo).
3. En la pestaña de variables de entorno de la aplicación, agregar
   `SERVICE_TOKEN` con el valor secreto elegido.
4. Desplegar. Coolify asigna una URL (por ejemplo `constancias.viscaya.cc`).
