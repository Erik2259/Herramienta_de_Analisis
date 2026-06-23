# Imagen base
FROM ubuntu:24.04

# Información del contenedor
LABEL maintainer="Erik"
LABEL version="0.1"
LABEL description="Contenedor para la app de Análisis de Datos"

# Sin confirmaciones interactivas de apt
ENV DEBIAN_FRONTEND=noninteractive

# Evita problemas de matplotlib sin pantalla
ENV MPLBACKEND=Agg

# Actualizar paquetes
RUN apt-get update

RUN apt-get upgrade -y

# Instalar Python y herramientas
RUN apt-get install -y python3 python3-pip python3-venv

# Directorio de trabajo
WORKDIR /home

# Copiar dependencias
COPY requirements.txt .

# Crear entorno virtual
RUN python3 -m venv venv

# Actualizar pip dentro del venv
RUN venv/bin/pip install --upgrade pip

# Instalar dependencias
RUN venv/bin/pip install -r requirements.txt

# Copiar la aplicación
COPY webapp ./webapp

# Puerto de la app
EXPOSE 8080

# Ejecutar la app
CMD ["venv/bin/streamlit", "run", "webapp/app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]