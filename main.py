import socket
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os
import urllib.request

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

hostname = socket.gethostname()

IPAddr = socket.gethostbyname(hostname)

port = int(os.environ.get('PORT', 5001))
app = Flask(__name__)

# Khởi tạo cơ sở dữ liệu SQLite
def create_db():
    conn = sqlite3.connect('fbAuto.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            avatar BLOB,
            timeuse DATE
        )
    ''')
    conn.commit()
    conn.close()

# Kiểm tra và tạo cơ sở dữ liệu nếu chưa tồn tại
create_db()

@app.route('/')
def index():
    # Lấy danh sách các liên hệ từ cơ sở dữ liệu
    conn = sqlite3.connect('fbAuto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        avatar = request.form['avatar']
        timeuse = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Thêm liên hệ vào cơ sở dữ liệu
        conn = sqlite3.connect('fbAuto.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (username, password, avatar, timeuse) VALUES (?, ?, ?, ?)', (username, password, avatar, timeuse))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    from waitress import serve
    print(IPAddr + ':' + str(5001))
    serve(app, host='0.0.0.0', port=5001)
