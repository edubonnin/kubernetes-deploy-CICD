FROM python:3.8-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copia las dependencias y las instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto 5000, donde se ejecuta Flask
EXPOSE 5000

ENV FLASK_APP=app.py
# Comando para inicial la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]