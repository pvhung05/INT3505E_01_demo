from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = "library.db"

# ------------------------------
# Hàm tiện ích
# ------------------------------
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


# ------------------------------
# Endpoint: Lấy danh sách sách + tìm kiếm + phân trang
# ------------------------------
@app.route("/books", methods=["GET"])
def get_books():
    author = request.args.get("author")
    category = request.args.get("category")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    query = "SELECT * FROM Book WHERE 1=1"
    params = []

    if author:
        query += " AND author LIKE ?"
        params.append(f"%{author}%")
    if category:
        query += " AND category LIKE ?"
        params.append(f"%{category}%")

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = query_db(query, params)
    books = [dict(row) for row in rows]

    return jsonify({
        "limit": limit,
        "offset": offset,
        "count": len(books),
        "data": books
    })


# ------------------------------
# ✅ Endpoint: Lấy danh sách thành viên + phân trang + tìm kiếm theo tên/email
# ------------------------------
@app.route("/members", methods=["GET"])
def get_members():
    name = request.args.get("name")
    email = request.args.get("email")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    query = "SELECT * FROM Member WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if email:
        query += " AND email LIKE ?"
        params.append(f"%{email}%")

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = query_db(query, params)
    members = [dict(row) for row in rows]

    return jsonify({
        "limit": limit,
        "offset": offset,
        "count": len(members),
        "data": members
    })


# ------------------------------
# Endpoint: Lấy thông tin 1 sách
# ------------------------------
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    row = query_db("SELECT * FROM Book WHERE id = ?", [book_id], one=True)
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Book not found"}), 404

# ------------------------------
# Endpoint: Lấy thông tin 1 người
# ------------------------------
@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    row = query_db("SELECT * FROM Member WHERE id = ?", [member_id], one=True)
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Member not found"}), 404


# ------------------------------
# Endpoint: Lấy danh sách phiếu mượn của 1 thành viên
# ------------------------------
@app.route("/members/<int:member_id>/loans", methods=["GET"])
def get_member_loans(member_id):
    status = request.args.get("status")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    query = "SELECT * FROM Loan WHERE member_id = ?"
    params = [member_id]

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = query_db(query, params)
    loans = [dict(row) for row in rows]
    return jsonify({
        "member_id": member_id,
        "limit": limit,
        "offset": offset,
        "data": loans
    })


# ------------------------------
# Khởi tạo DB & seed dữ liệu
# ------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Book (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    category TEXT,
                    status TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Member (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Librarian (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    employee_code TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Loan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    member_id INTEGER,
                    librarian_id INTEGER,
                    borrow_date TEXT,
                    return_date TEXT,
                    status TEXT,
                    FOREIGN KEY (book_id) REFERENCES Book(id),
                    FOREIGN KEY (member_id) REFERENCES Member(id),
                    FOREIGN KEY (librarian_id) REFERENCES Librarian(id)
                )''')
    conn.commit()
    conn.close()


def seed_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Xóa dữ liệu cũ (nếu muốn reset)
    c.execute("DELETE FROM Loan")
    c.execute("DELETE FROM Member")
    c.execute("DELETE FROM Book")
    c.execute("DELETE FROM Librarian")

    # Thêm dữ liệu Book
    c.executemany("""
        INSERT INTO Book (title, author, category, status)
        VALUES (?, ?, ?, ?)
    """, [
        ('Dế Mèn Phiêu Lưu Ký', 'Tô Hoài', 'Thiếu nhi', 'available'),
        ('O Chuột', 'Tô Hoài', 'Văn học', 'borrowed'),
        ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 'Fantasy', 'available'),
        ('To Kill a Mockingbird', 'Harper Lee', 'Classic', 'available'),
        ('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 'borrowed'),
    ])

    # Thêm dữ liệu Member
    c.executemany("""
        INSERT INTO Member (name, email)
        VALUES (?, ?)
    """, [
        ('Nguyễn Văn A', 'vana@example.com'),
        ('Trần Thị B', 'thib@example.com'),
        ('Lê Văn C', 'vanc@example.com')
    ])

    # Thêm dữ liệu Librarian
    c.executemany("""
        INSERT INTO Librarian (name, email, employee_code)
        VALUES (?, ?, ?)
    """, [
        ('Phạm Thị Thư', 'thu.librarian@example.com', 'EMP001'),
        ('Ngô Văn Minh', 'minh.lib@example.com', 'EMP002')
    ])

    # Thêm dữ liệu Loan
    c.executemany("""
        INSERT INTO Loan (book_id, member_id, borrow_date, return_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 1, '2025-10-01', '2025-10-10', 'returned'),
        (2, 1, '2025-10-05', None, 'borrowed'),
        (5, 2, '2025-10-07', None, 'overdue')
    ])

    conn.commit()
    conn.close()


# ------------------------------
# Chạy app
# ------------------------------
if __name__ == "__main__":
    init_db()
    seed_data()
    app.run(debug=True)
