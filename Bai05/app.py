from flask import Flask, request, jsonify
import sqlite3
import base64, json

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


# ======================================================
# 1️⃣ OFFSET–LIMIT PAGINATION (GIỮ NGUYÊN)
# ======================================================
@app.route("/books", methods=["GET"])
def get_books_offset():
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
        "type": "offset-limit",
        "limit": limit,
        "offset": offset,
        "count": len(books),
        "data": books
    })


# ======================================================
# 2️⃣ PAGE-BASED PAGINATION
# ======================================================
@app.route("/books/page", methods=["GET"])
def get_books_page():
    author = request.args.get("author")
    category = request.args.get("category")
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    offset = (page - 1) * size

    query = "SELECT * FROM Book WHERE 1=1"
    params = []

    if author:
        query += " AND author LIKE ?"
        params.append(f"%{author}%")
    if category:
        query += " AND category LIKE ?"
        params.append(f"%{category}%")

    query += " LIMIT ? OFFSET ?"
    params.extend([size, offset])

    rows = query_db(query, params)
    books = [dict(row) for row in rows]

    total = query_db("SELECT COUNT(*) as total FROM Book", one=True)["total"]
    total_pages = (total + size - 1) // size

    return jsonify({
        "type": "page-based",
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "count": len(books),
        "data": books
    })


# ======================================================
# 3️⃣ CURSOR-BASED PAGINATION
# ======================================================
@app.route("/books/cursor", methods=["GET"])
def get_books_cursor():
    limit = int(request.args.get("limit", 5))
    cursor = request.args.get("cursor")

    # Giải mã cursor (nếu có)
    last_id = 0
    if cursor:
        try:
            decoded = base64.b64decode(cursor).decode("utf-8")
            last_id = json.loads(decoded).get("last_id", 0)
        except Exception:
            return jsonify({"error": "Invalid cursor"}), 400

    # Lấy dữ liệu mới hơn cursor
    query = "SELECT * FROM Book WHERE id > ? ORDER BY id ASC LIMIT ?"
    rows = query_db(query, [last_id, limit])
    books = [dict(row) for row in rows]

    # Tạo cursor mới nếu còn dữ liệu
    next_cursor = None
    if len(books) == limit:
        last_book_id = books[-1]["id"]
        cursor_data = json.dumps({"last_id": last_book_id})
        next_cursor = base64.b64encode(cursor_data.encode()).decode()

    return jsonify({
        "type": "cursor-based",
        "limit": limit,
        "next_cursor": next_cursor,
        "data": books
    })


# ======================================================
# Các endpoint cũ (giữ nguyên)
# ======================================================
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


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    row = query_db("SELECT * FROM Book WHERE id = ?", [book_id], one=True)
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Book not found"}), 404


@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    row = query_db("SELECT * FROM Member WHERE id = ?", [member_id], one=True)
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Member not found"}), 404


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


# ======================================================
# Khởi tạo DB & seed dữ liệu
# ======================================================
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
    c.execute("DELETE FROM Loan")
    c.execute("DELETE FROM Member")
    c.execute("DELETE FROM Book")
    c.execute("DELETE FROM Librarian")

    c.executemany("""
        INSERT INTO Book (title, author, category, status)
        VALUES (?, ?, ?, ?)
    """, [
        ('Book A', 'Author 1', 'Category X', 'available'),
        ('Book B', 'Author 2', 'Category Y', 'available'),
        ('Book C', 'Author 3', 'Category Z', 'available'),
        ('Book D', 'Author 4', 'Category X', 'available'),
        ('Book E', 'Author 5', 'Category Y', 'available'),
        ('Book F', 'Author 6', 'Category Z', 'available'),
        ('Book G', 'Author 7', 'Category X', 'available'),
        ('Book H', 'Author 8', 'Category Y', 'available'),
        ('Book I', 'Author 9', 'Category Z', 'available'),
        ('Book J', 'Author 10', 'Category X', 'available')
    ])

    c.executemany("""
        INSERT INTO Member (name, email)
        VALUES (?, ?)
    """, [
        ('Nguyễn Văn A', 'vana@example.com'),
        ('Trần Thị B', 'thib@example.com'),
        ('Lê Văn C', 'vanc@example.com')
    ])

    conn.commit()
    conn.close()


# ======================================================
# Chạy app
# ======================================================
if __name__ == "__main__":
    init_db()
    seed_data()
    app.run(debug=True)
