import os
from pathlib import Path
import dotenv
from abc import ABC, abstractmethod  # new
# import psycopg2
import mysql.connector
from app.models import NewsDB, NewsSchema  # new

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / ".env")


class Database(ABC):
    """
    Database context manager
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


class MyDatabase(Database):
    """PostgreSQL Database context manager"""

    def __init__(self) -> None:
        self.driver = mysql.connector
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            buffered=True,
            # dictionary=True
            # named_tuple = True,
        )


