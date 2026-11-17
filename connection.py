
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

required_settings = {
    "DB_HOST": DB_HOST,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_NAME": DB_NAME,
}

missing = [key for key, value in required_settings.items() if value is None]

if missing:
    raise ValueError(f"Missing database settings: {', '.join(missing)}")

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT DATABASE(), VERSION()")
            )

            database, version = result.fetchone()

            print("Database connection successful!")
            print(f"Database: {database}")
            print(f"MySQL Version: {version}")

            return True

    except Exception as error:
        print(f"Database connection failed: {error}")
        return False


if __name__ == "__main__":
    test_connection()
