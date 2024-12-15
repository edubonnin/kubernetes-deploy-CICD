import pytest
import psycopg2
import redis

from app.app import get_db_connection, get_cache_connection


def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        assert cursor.fetchone() == (1,)
    finally:
        cursor.close()
        conn.close()


def test_redis_connection():
    try:
        r = get_cache_connection()
        assert r.ping()  # El comando ping debe retornar True si Redis está accesible
    except redis.ConnectionError:
        pytest.fail("Failed to connect to Redis")
