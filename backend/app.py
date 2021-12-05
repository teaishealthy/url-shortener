import sqlite3
import re

from .bootstrap import get_base_folder_path

from flask import Flask, redirect
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
with open(f'{get_base_folder_path()}/../frontend/index.html', 'r') as f:
    index_data = f.read()
@app.post('/short/<path:url>')
def create_short(url: str):
    if not pattern.match(url):
        return {"error": "Invalid URL"}, 400
    connection = sqlite3.connect(f'{get_base_folder_path()}/database.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO shorts (link) VALUES (?)', (url,))
    connection.commit()
    connection.close()
    return {'url': f'/short/{cursor.lastrowid}'}

@app.get('/short/<path:short_id>')
def get_short(short_id: int):
    return redirect(_get_short(short_id))

@app.get('/expand/<path:short_id>/')
def expand_short(short_id: int):
    return _get_short(short_id)

@app.get('/')
def index():
    return index_data

def _get_short(short_id: int):
    connection = sqlite3.connect(f'{get_base_folder_path()}/database.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT link FROM shorts WHERE id = ?', (short_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]
@app.delete('/short/<path:short_id>')
def delete_short(short_id: int):
    connection = sqlite3.connect(f'{get_base_folder_path()}/database.db')
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM shorts WHERE id = ?', (short_id,))
    # check if row was deleted
    if cursor.rowcount == 0:
        connection.close()
        return {"error": "Short link not found"}, 404
    connection.commit()
    connection.close()
    return {'success': True}

if __name__ == '__main__':
    app.run(debug=True)
