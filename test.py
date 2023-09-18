import sqlite3

# Khởi tạo cơ sở dữ liệu SQLite


# Kiểm tra và tạo cơ sở dữ liệu nếu chưa tồn tại
create_db()

# Lấy danh sách các liên hệ từ cơ sở dữ liệu
def get_contacts():
    conn = sqlite3.connect('danhba.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    return contacts

# Thêm liên hệ vào cơ sở dữ liệu
def add_contact(name, phone):
    conn = sqlite3.connect('danhba.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    conn.commit()
    conn.close()
