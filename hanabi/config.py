import os


def get_db_url():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "postgres")

    return f"postgres://{user}:{password}@{host}:{port}/{database}"


def get_secret_key():
    secret_key = os.getenv("SECRET_KEY", None)
    is_debug = os.getenv("FLASK_ENV", "").lower() == "development"
    if not secret_key and is_debug:
        secret_key = "dev"

    return secret_key


class Config:
    SECRET_KEY = get_secret_key()

    SQLALCHEMY_DATABASE_URI = get_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
