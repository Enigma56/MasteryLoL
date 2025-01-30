import os

# TODO: Load the environment variables in app/__init__.py
def create_db_url(turso_db_url, turso_auth_token) -> str:
    TURSO_DATABASE_URL = turso_db_url
    TURSO_AUTH_TOKEN = turso_auth_token
    dbURL = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=True"

    return dbURL
