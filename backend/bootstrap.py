import os
import sqlite3
from contextlib import contextmanager


def get_base_folder_path():
    return os.path.dirname(os.path.abspath(__file__))


@contextmanager
def connection():
    connection = sqlite3.connect(f"{get_base_folder_path()}/database.db")
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception:
        # Rollback in case there is any error
        connection.rollback()
    finally:
        connection.close()


def bootstrap():
    with connection() as cursor:
        with open(f"{get_base_folder_path()}/bootstrap.sql", "r") as file:
            cursor.executescript(file.read())


if __name__ == "__main__":
    bootstrap()
