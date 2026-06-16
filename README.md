# Herramienta_de_Analisis

# 1ra Etapa: Carga y Análisis de Datos

## Herramienta de Análisis
### Módulo: Descripción

* **Carga de archivos CSV**
* **Validación del archivo**
  * Debe cumplir con una estructura específica.
* **Análisis descriptivo**
  * Número de filas.
  * Número de columnas.
  * Tipos de datos por columna.
  * Valores nulos por columna.
  * Estadísticas descriptivas:
    * Valores únicos.
    * Máximos y mínimos.
    * Media.
    * Mediana.
    * Moda.
* **Gráficas**
  * Mapa de calor (Matriz de correlación / Faltantes).

  ## 🛠️ Guía de Desarrollo y Actualización

A continuación, se detallan los comandos de uso frecuente para guardar el progreso en el repositorio y gestionar las actualizaciones del contenedor Docker.

### 💾 1. Guardar cambios en GitHub (Commit & Push)
Sigue este orden para subir tus actualizaciones de código al repositorio:
* **Verificar el estado:** Ejecuta `git status` para ver los archivos modificados.
* **Preparar los archivos:** Ejecuta `git add .` para agregar todos los cambios.
* **Crear el commit:** Ejecuta `git commit -m "mensaje descriptivo"` para guardar en el historial local.
* **Subir los cambios:** Ejecuta `git push` para enviar tus actualizaciones a GitHub.

### 🐳 2. Actualizar el Contenedor Docker (Flujo Estándar)
Si agregas nuevas librerías en `requirements.txt` o modificas el `Dockerfile`, debes aplicar un ciclo completo de actualización:
1. **Detener la instancia activa:** `docker stop contenedor_analisis`
2. **Eliminar el contenedor:** `docker rm contenedor_analisis`
3. **Reconstruir la imagen:** `docker build -t app-analisis-datos:v1 .`
4. **Ejecutar el contenedor actualizado:** `docker run -d -p 8501:8501 --name contenedor_analisis app-analisis-datos:v1`

### ⚡ 3. Modo Desarrollo en Tiempo Real (Volúmenes)
Para ver los cambios de tu código (`app.py`) en vivo sin tener que reconstruir la imagen de Docker a cada momento, ejecuta el contenedor sincronizando tu directorio local:

* **Comando para desarrollo en vivo:**
```bash
  docker run -d -p 8501:8501 -v $(pwd):/app --name contenedor_analisis app-analisis-datos:v1