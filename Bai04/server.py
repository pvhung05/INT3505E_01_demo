from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# -------------------------------
# Cấu hình JWT và Swagger
# -------------------------------
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["SWAGGER"] = {
    "title": "Book Management API",
    "uiversion": 3
}

jwt = JWTManager(app)
swagger = Swagger(app, template_file='openapi.yaml')

# -------------------------------
# Database giả lập
# -------------------------------
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999},
    {"id": 3, "title": "Refactoring", "author": "Martin Fowler", "year": 1999}
]

# -------------------------------
# Endpoint đăng nhập (JWT)
# -------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get("username") == "admin" and data.get("password") == "123":
        token = create_access_token(identity="admin")
        return jsonify(access_token=token)
    return jsonify({"msg": "Sai thông tin đăng nhập"}), 401

# -------------------------------
# Các endpoint có bảo vệ JWT
# -------------------------------
@app.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    author = request.args.get('author')
    limit = int(request.args.get('limit', 10))
    books = BOOKS
    if author:
        books = [b for b in books if author.lower() in b['author'].lower()]
    return jsonify(books[:limit])

@app.route('/books/<int:id>', methods=['GET'])
@jwt_required()
def get_book(id):
    for book in BOOKS:
        if book['id'] == id:
            return jsonify(book)
    return jsonify({"message": "Không tìm thấy"}), 404

@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.json
    new_book = {
        "id": len(BOOKS) + 1,
        "title": data["title"],
        "author": data["author"],
        "year": data["year"]
    }
    BOOKS.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    data = request.json
    for book in BOOKS:
        if book['id'] == id:
            book.update(data)
            return jsonify(book)
    return jsonify({"message": "Không tìm thấy"}), 404

@app.route('/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    global BOOKS
    BOOKS = [b for b in BOOKS if b['id'] != id]
    return '', 204

if __name__ == '__main__':
    app.run(port=5000, debug=True)
