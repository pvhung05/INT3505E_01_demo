from flask import Flask, jsonify, request

app = Flask(__name__)

# Dữ liệu sách lưu trong dictionary, key là id
books = {
    1: {"title": "Python co ban", "author": "Nguyen Van A", "available": True},
    2: {"title": "Giai thuat lap trinh", "author": "TTran Van B", "available": True},
}

# -------------------------------
# API endpoints
# -------------------------------

# Lấy danh sách tất cả sách
@app.route("/books", methods=["GET"])
def list_books():
    return jsonify([
        {"id": book_id, **info} for book_id, info in books.items()
    ])

# Lấy thông tin 1 cuốn sách
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    if book_id not in books:
        return "Không tìm thấy sách", 404
    return jsonify({"id": book_id, **books[book_id]})

# Tìm sách theo tên
@app.route("/search", methods=["GET"])
def search_books():
    query = request.args.get("title", "").lower()
    results = [
        {"id": book_id, **info}
        for book_id, info in books.items()
        if query in info["title"].lower()
    ]
    return jsonify(results)

# Thêm sách mới
@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    if not data or "title" not in data or "author" not in data:
        return "Thiếu dữ liệu", 400

    new_id = max(books.keys(), default=0) + 1
    books[new_id] = {
        "title": data["title"],
        "author": data["author"],
        "available": True,
    }
    return jsonify({"id": new_id, **books[new_id]}), 201

# Cập nhật thông tin sách
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    if book_id not in books:
        return "Không tìm thấy sách", 404
    
    data = request.json
    books[book_id].update({k: v for k, v in data.items() if k in ["title", "author", "available"]})
    return jsonify({"id": book_id, **books[book_id]})

# Xóa sách
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    if book_id not in books:
        return "Không tìm thấy sách", 404
    
    del books[book_id]
    return "Xóa thành công", 200

# Cập nhật trạng thái sách (mượn hoặc trả)
@app.route("/books/<int:book_id>/status", methods=["POST"])
def update_status(book_id):
    if book_id not in books:
        return "Không tìm thấy sách", 404

    action = request.json.get("action")
    if action == "borrow":
        if not books[book_id]["available"]:
            return "Sách đã được mượn", 400
        books[book_id]["available"] = False
    elif action == "return":
        if books[book_id]["available"]:
            return "Sách chưa được mượn", 400
        books[book_id]["available"] = True
    else:
        return "Hành động không hợp lệ", 400

    return jsonify({"id": book_id, **books[book_id]})

# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
