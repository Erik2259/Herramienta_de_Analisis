# Definir la imagen base
FROM ubuntu:24.04
#Informacion del contenedor
LABEL maintainer="Erik"
LABEL version="0.1"
LABEL description="contenedor para desarrollo en Python 3.12"

#Instalar paquetes
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 -y
COPY requirements.txt /home/requirements.txt
RUN pip install -r requirements
COPY webapp /home/webapp