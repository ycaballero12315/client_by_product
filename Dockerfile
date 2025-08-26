FROM python:3.13-slim

# Variables de entorno
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 

# Directorio de trabajo
WORKDIR /app

# Copiar requirements y crear venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando por defecto para producción
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
