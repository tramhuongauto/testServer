import socket
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import sqlite3
from datetime import datetime
import os


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
    users = cursor.fetchone()
    conn.close()
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        if request.form['key'] == 'VTGR915d4578*#':
            username = request.form['username']
            password = request.form['password']
            avatar = request.files['images']
            avatar.save('static/' + avatar.filename) 
            timeuse = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Thêm liên hệ vào cơ sở dữ liệu
            conn = sqlite3.connect('fbAuto.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
            users = cursor.fetchall()
            if len(users) > 0:
                return render_template('index.html', users=username, password=password, error="Tên đã tồn tại")
            cursor.execute('INSERT INTO users (username, password, avatar, timeuse) VALUES (?, ?, ?, ?)', (username, password, url_for('http://116.98.166.53:5001/static', filename=avatar.filename), timeuse))
            conn.commit()
            conn.close()
        else:
            abort(400, 'Bạn không có quyền ở đây')

    return redirect(url_for('index'))

@app.route('/api/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    conn = sqlite3.connect('fbAuto.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
    row = cursor.fetchone()
    if row is None or password != row[1]:  
        return jsonify({'id': row[0], 'result': 'False', 'time': '', 'avatar': row[3]})
    
    else:
        current_date = datetime.today()
        expiration_date = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
        days_remaining = (expiration_date - current_date).days
        return jsonify({'id': row[0], 'result': 'Pass', 'time': days_remaining, 'avatar': row[3]})

@app.route('/api/update-image', methods=['POST'])
def updateImage():
    id = request.form['id']
    print(id)
    file = request.files['avatar']
    if file.filename.split('.')[-1] not in ['png', 'jpg', 'jpeg']:
        return jsonify({'id': id, 'result': 'Fail', 'time': '', 'avatar':  ''})
    
    else:
        try:
            file.save('static/' + file.filename)
            conn = sqlite3.connect('fbAuto.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET avatar = (?) WHERE id = (?)', ('http://116.98.166.53:5001/static/' + file.filename, id))
            conn.commit()
            return jsonify({'id': id, 'result': 'OK', 'time': '', 'avatar':  'http://116.98.166.53:5001/static/' + file.filename})
        except:
            return jsonify({'id': id, 'result': 'Fail', 'time': '', 'avatar': ''})
    
if __name__ == "__main__":
    from waitress import serve
    print(IPAddr + ':' + str(5001))
    serve(app, host='0.0.0.0', port=5001)
