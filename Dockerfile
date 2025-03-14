# Usa la imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

RUN chmod +x /app/entrypoint.sh

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000
