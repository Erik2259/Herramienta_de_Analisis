# ==========================================
# Imagen base
# ==========================================
FROM ubuntu:24.04

# ==========================================
# Información del contenedor
# ==========================================
LABEL maintainer="Erik"
LABEL version="0.1"
LABEL description="Contenedor para la app de Análisis de Datos (Python 3.12 + Streamlit)"

# Evita que apt-get pida confirmaciones interactivas durante el build
ENV DEBIAN_FRONTEND=noninteractive
# Evita problemas de backend gráfico de matplotlib dentro del contenedor
ENV MPLBACKEND=Agg

# ==========================================
# Instalar Python, pip y herramientas de entorno virtual
# ==========================================
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ==========================================
# Directorio de trabajo
# ==========================================
WORKDIR /home

# ==========================================
# Copiar requirements primero (mejor cacheo de capas de Docker)
# ==========================================
COPY requirements.txt /home/requirements.txt

# ==========================================
# Crear el entorno virtual e instalar las dependencias dentro de él
# ==========================================
RUN python3 -m venv /home/venv
RUN /home/venv/bin/pip install --upgrade pip && \
    /home/venv/bin/pip install --no-cache-dir -r /home/requirements.txt

# ==========================================
# Copiar el código de la aplicación
# ==========================================
COPY webapp /home/webapp

# ==========================================
# Puerto que expondrá el contenedor
# ==========================================
EXPOSE 8080

# ==========================================
# Comando por defecto: ejecutar la app con Streamlit usando el venv
# ==========================================
CMD ["/home/venv/bin/streamlit", "run", "/home/webapp/app.py", \
     "--server.port=8080", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]