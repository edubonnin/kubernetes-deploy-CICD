import json
import time
from flask import Flask, Response, render_template
import psycopg2
import logging
import redis
import os
import socket

app = Flask(__name__)


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


@app.route('/healthz', methods=['GET'])
def healthz():
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Asumimos que la app está saludable si se ejecuta este código
    app_status = "healthy"

    # Verificar base de datos
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1;')
        db_status = "healthy"
        cur.close()
        conn.close()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # Verificar caché
    try:
        r = get_cache_connection()
        r.ping()
        cache_status = "healthy"
    except Exception as e:
        cache_status = f"unhealthy: {str(e)}"

    # Determinar estado global
    # Si DB o Cache están en estado "unhealthy", el overall pasa a "unhealthy"
    overall_status = "healthy"
    if not (db_status == "healthy" and cache_status == "healthy"):
        overall_status = "unhealthy"

    response = {
        "status": overall_status,
        "timestamp": timestamp,
        "components": {
            "application": app_status,
            "database": db_status,
            "cache": cache_status
        }
    }

    json_response = json.dumps(response)
    # Si hay algún componente crítico en "unhealthy", devolver 503
    status_code = 200 if overall_status == "healthy" else 503

    return Response(json_response, status=status_code, mimetype='application/json')


if __name__ == '__main__':
    # Usar el host correcto para asegurar que la aplicación sea accesible desde fuera del contenedor
    app.run(host='0.0.0.0', port=5000)
