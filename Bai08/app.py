from flask import Flask, jsonify, request

app = Flask(__name__)

books = []
next_id = 1

# 1️⃣ Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# 2️⃣ Add a book
@app.route('/books', methods=['POST'])
def add_book():
    global next_id
    data = request.get_json()
    book = {
        "id": next_id,
        "title": data.get('title'),
        "author": data.get('author')
    }
    books.append(book)
    next_id += 1
    return jsonify(book), 201

# 3️⃣ Get a single book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# 4️⃣ Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    for book in books:
        if book["id"] == book_id:
            book["title"] = data.get('title', book['title'])
            book["author"] = data.get('author', book['author'])
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# 5️⃣ Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    for book in books:
        if book["id"] == book_id:
            books = [b for b in books if b["id"] != book_id]
            return jsonify({"message": "Book deleted"}), 200
    return jsonify({"error": "Book not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
