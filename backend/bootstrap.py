import os
import sqlite3

def get_base_folder_path():
    return os.path.dirname(os.path.abspath(__file__))

def bootstrap():
    connection = sqlite3.connect(f'{get_base_folder_path()}/database.db')
    cursor = connection.cursor()
    with open(f'{get_base_folder_path()}/bootstrap.sql', 'r') as file:
        cursor.executescript(file.read())
    connection.commit()
    connection.close()

if __name__ == '__main__':
    bootstrap()