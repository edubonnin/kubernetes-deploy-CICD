from unittest.mock import patch, MagicMock
from app.app import get_db_connection, get_cache_connection

# Test de la conexión a la base de datos con mocking completo


def test_db_connection():
    with patch('psycopg2.connect') as mock_connect, \
            patch.dict('os.environ', {
                'POSTGRES_HOST': 'localhost',
                'POSTGRES_PORT': '5432',
                'POSTGRES_USER': 'user',
                'POSTGRES_PASSWORD': 'password',
                'POSTGRES_DB': 'testdb'
            }):
        mock_connect.return_value = MagicMock()
        conn = get_db_connection()
        assert conn is not None
        mock_connect.assert_called_with(
            host='localhost',
            port='5432',
            user='user',
            password='password',
            database='testdb'
        )

# Test de la conexión Redis con mocking completo


def test_redis_connection():
    with patch('redis.Redis.ping', return_value=True), \
            patch.dict('os.environ', {
                'REDIS_HOST': 'localhost',
                'REDIS_PORT': '6379'
            }):
        r = get_cache_connection()
        assert r.ping() is True
