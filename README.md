
# 📊 Herramienta de Análisis de Datos — Etapa 1
 
Aplicación web hecha con **Streamlit** que permite cargar un archivo CSV y obtener
automáticamente: validación de estructura, estadísticas descriptivas, mapas de calor
(correlación y valores faltantes) y gráficas individuales por variable.
 
Este proyecto está **dockerizado**, de modo que cualquier persona puede ejecutar la
aplicación con un solo comando, sin instalar Python ni dependencias manualmente.
 
---
 
## 📁 Estructura del proyecto
 
```
.
├── webapp/
│   └── app.py            # Código de la aplicación Streamlit
├── Dockerfile             # Receta para construir la imagen de Docker
├── .dockerignore           # Archivos que no se copian a la imagen
├── requirements.txt        # Dependencias de Python con versiones fijas
├── LICENSE
└── README.md
```
 
---
 
## ✅ Requisitos previos
 
- Tener una cuenta en [Docker Hub](https://hub.docker.com/).
- Trabajar dentro de un **GitHub Codespace** (ya trae Docker preinstalado) o tener
  Docker Desktop instalado localmente.
- Verificar que Docker esté disponible:
```bash
docker --version
```
 
---
 
## 🐍 Paso 0 (opcional): Generar `requirements.txt` desde la terminal
 
Si en algún momento cambias las librerías que usa tu app y necesitas regenerar el
archivo `requirements.txt` reflejando exactamente lo que tienes instalado, hazlo así
dentro del Codespace:
 
```bash
# 1. Crear el entorno virtual
python3 -m venv venv
 
# 2. Activar el entorno virtual
source venv/bin/activate
 
# 3. Instalar las librerías que usa la app
pip install streamlit pandas matplotlib seaborn
 
# 4. Congelar las versiones instaladas en requirements.txt
pip freeze > requirements.txt
 
# 5. Salir del entorno virtual
deactivate
```
 
> 💡 Este `venv` es solo para **desarrollo local** (probar la app fuera de Docker).
> No se copia dentro de la imagen — el Dockerfile crea su **propio** entorno virtual
> dentro del contenedor, por eso `venv/` está en `.dockerignore`.
 
Si quieres probar la app sin Docker, en este punto ya podrías ejecutar:
 
```bash
streamlit run webapp/app.py
```
 
---
 
## 🐳 Paso 1: Construir la imagen Docker
 
Desde la raíz del proyecto (donde está el `Dockerfile`), ejecuta:
 
```bash
docker build -t analisis-datos:1.0 .
```
 
- `-t analisis-datos:1.0` → nombre (`analisis-datos`) y etiqueta/versión (`1.0`) de la imagen.
- `.` → indica que el contexto de build es la carpeta actual.
Verifica que la imagen se creó correctamente:
 
```bash
docker images
```
 
---
 
## ▶️ Paso 2: Ejecutar el contenedor localmente
 
```bash
docker run -d --name analisis-datos-app -p 8080:8080 analisis-datos:1.0
```
 
- `-d` → ejecuta el contenedor en segundo plano (detached).
- `--name analisis-datos-app` → nombre del contenedor.
- `-p 8080:8080` → mapea el puerto 8080 del contenedor al puerto 8080 de tu máquina.
- `analisis-datos:1.0` → la imagen que acabas de construir.
Abre la app en el navegador: **http://localhost:8080**
 
> En GitHub Codespaces, ve a la pestaña **"Ports"** y abre el puerto `8080`
> (Codespaces te dará una URL pública automáticamente).
 
Comandos útiles para administrar el contenedor:
 
```bash
docker ps                          # Ver contenedores corriendo
docker logs analisis-datos-app     # Ver logs de la app
docker stop analisis-datos-app     # Detener el contenedor
docker rm analisis-datos-app       # Eliminar el contenedor
```
 
---
 
## ☁️ Paso 3: Subir la imagen a Docker Hub
 
1. Inicia sesión en Docker Hub desde la terminal:
```bash
docker login
```
 
2. Etiqueta tu imagen con tu usuario de Docker Hub (reemplaza `tu_usuario`):
```bash
docker tag analisis-datos:1.0 tu_usuario/analisis-datos:1.0
```
 
3. Sube (push) la imagen:
```bash
docker push tu_usuario/analisis-datos:1.0
```
 
4. Verifica que tu imagen ya aparece en tu perfil de Docker Hub:
   `https://hub.docker.com/r/tu_usuario/analisis-datos`
---
 
## 📥 Paso 4: Cómo cualquier persona puede usar tu app
 
Una vez publicada, cualquiera puede descargar y ejecutar tu app con dos comandos:
 
```bash
docker pull tu_usuario/analisis-datos:1.0
docker run -d --name=analisis-datos-app -p 8080:8080 tu_usuario/analisis-datos:1.0
```
 
Luego solo abre **http://localhost:8080** en el navegador y la herramienta de
análisis de datos estará lista para usarse, sin instalar Python ni ninguna librería.
 
---
 
## 🛠️ Notas técnicas del Dockerfile
 
- Se usa `ubuntu:24.04` como imagen base, que trae **Python 3.12**.
- Se crea un **entorno virtual** dentro de la imagen (`/home/venv`) y todas las
  dependencias de `requirements.txt` se instalan ahí, en lugar de instalarlas a nivel
  de sistema (buena práctica y evita conflictos con el Python del sistema operativo).
- `requirements.txt` se copia **antes** que el código de la app para aprovechar el
  cacheo de capas de Docker: si solo cambias `app.py`, no se reinstalan las
  dependencias en el siguiente build.
- El contenedor expone y sirve la app en el puerto **8080** (`--server.port=8080
  --server.address=0.0.0.0`), por eso el mapeo `-p 8080:8080` funciona directo.
---
 
## 📝 Licencia
 
Este proyecto se distribuye bajo los términos especificados en el archivo [LICENSE](./LICENSE).
 

