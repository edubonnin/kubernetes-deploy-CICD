from flask import Flask, render_template
import psycopg2
import logging
import redis
import os
import socket

app = Flask(__name__)

# Configurar Flask dependiendo de la variable de entorno
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = app.config['ENV'] == 'development'


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            database=os.environ['POSTGRES_DB']
        )
        return conn
    except KeyError as e:
        raise RuntimeError(
            "Error de configuración: Falta la variable de entorno requerida") from e


def get_cache_connection():
    try:
        host = os.environ['REDIS_HOST']
        port = int(os.environ['REDIS_PORT'])
    except KeyError as e:
        # Maneja la falta de variables de entorno
        raise RuntimeError(
            f"La variable de entorno {e.args[0]} no está definida"
        ) from e
    except ValueError:
        # Maneja el error de conversión
        raise ValueError("El puerto debe ser un número entero")

    return redis.Redis(host=host, port=port, db=0)


def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios;')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


@app.route('/')
def index():
    db_conn = get_db_connection()
    db_status = 'Connected' if db_conn else 'Not Connected'
    db_conn.close()

    try:
        cache_conn = get_cache_connection()
        cache_status = 'Connected' if cache_conn.ping() else 'Not Connected'

        # Intentar obtener el mensaje desde Redis
        cache_message = cache_conn.get('mensaje')
        if cache_message:
            cache_message = cache_message.decode('utf-8')
        else:
            cache_message = 'No hay mensaje en Redis'
    except Exception as e:
        logging.error(f"Error al interactuar con Redis: {e}")
        cache_status = 'Not Connected'
        cache_message = 'No Cache'

    try:
        data = get_data()
    except Exception as e:
        logging.error(f"Error obteniendo datos: {e}")
        data = []

    hostname = socket.gethostname()  # Obtener el nombre del host

    return render_template('index.html', db_status=db_status, cache_status=cache_status, data=data, cache_message=cache_message, hostname=hostname)


if __name__ == '__main__':
    # Usar el host correcto para asegurar que la aplicación sea accesible desde fuera del contenedor
    app.run(host='0.0.0.0', port=5000)
