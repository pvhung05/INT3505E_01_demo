from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Lập trình Python", "author": "Nguyễn Văn A", "available": True},
    {"id": 2, "title": "Cấu trúc dữ liệu", "author": "Trần Văn B", "available": True},
]

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    for b in books:
        if b["id"] == book_id:
            book = b;
            break
    if book:
        return jsonify(book)
    else:
        return "Not Found", 404

@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    
    if len(books) > 0:  
        max_id = 0
    for b in books:
        if b["id"] > max_id:
        # Nếu đã có sách thì lấy id lớn nhất + 1
            max_id = b["id"]
            new_id = max_id + 1
        else:
        # Nếu chưa có sách nào thì id bắt đầu từ 1
            new_id = 1

    book = {
    "id": new_id,
    "title": data["title"],
    "author": data["author"],
    "available": True   }

    books.append(book)
    return jsonify(book), 201

# Cập nhật thông tin sách
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    for b in books:
        if b["id"] == book_id:
            book = b
            break
    
    if book is None:
        return "Không tìm thấy sách", 404
    
    data = request.json

    for key in data:
        book[key] = data[key]

    return jsonify(book)
    
# Xóa sách
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    found = False
    new_books = []
    for b in books:
        if b["id"] == book_id:
            found = True
            # bỏ qua cuốn sách này, tức là xóa
            continue
        new_books.append(b)
    
    if not found:
        return "Không tìm thấy sách", 404
    
    books = new_books
    return "Xóa thành công", 200

# Mượn sách
@app.route("/borrow/<int:book_id>", methods=["POST"])
def borrow_book(book_id):
    book = None
    for b in books:
        if b["id"] == book_id:
            book = b
            break

    if book is None:
        return "Không tìm thấy sách", 404

    # Kiểm tra tình trạng sách
    if not book["available"]:
        return "Sách đã được mượn", 400

    # Đánh dấu sách là đã mượn
    book["available"] = False
    return jsonify(book)

# Trả sách
@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    book = None
    for b in books:
        if b["id"] == book_id:
            book = b
            break

    if book is None:
        return "Không tìm thấy sách", 404

    # Kiểm tra tình trạng
    if book["available"]:
        return "Sách chưa được mượn", 400

    # Đánh dấu sách là có sẵn
    book["available"] = True
    return jsonify(book)

# -------------------------------
# Chạy server
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)
