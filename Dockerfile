# Usar una imagen base ligera de Python
FROM python:3.10-slim

# Evitar que Python escriba archivos .pyc en el disco y asegurar salida en consola limpia
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar herramientas del sistema necesarias para compilar ciertas librerías si fuera necesario
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar los requerimientos antes del resto del código para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY . .

# Exponer el puerto nativo de Streamlit
EXPOSE 8501

# Monitoreo de salud del contenedor
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Comando para arrancar Streamlit vinculando la dirección IP correcta
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]