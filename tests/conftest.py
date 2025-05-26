import os
import psycopg2
import pytest

@pytest.fixture(scope='session')
def db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER", "test_user"),
        password=os.getenv("DB_PASS")
    )
    yield conn
    conn.close()

@pytest.fixture
def cursor(db_connection):
    with db_connection.cursor() as cur:
        yield cur