import pytest
import redis
from unittest.mock import patch, MagicMock
from app.app import get_db_connection, get_cache_connection


def test_db_connection():
    with patch('psycopg2.connect') as mock_connect:
        mock_connect.return_value = MagicMock()
        conn = get_db_connection()
        assert conn is not None


def test_redis_connection():
    with patch('redis.Redis.ping', return_value=True):
        r = get_cache_connection()
        assert r.ping() == True
