# Usa una imagen base de Python
FROM python:3.11

# Establecer el directorio de trabajo dentro de la app
WORKDIR /app

# Copiar solo el archivo requirements.txt primero para aprovechar la caché
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto 8000 para el servidor Django
EXPOSE 8000

# Ejecutar el servidor de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
