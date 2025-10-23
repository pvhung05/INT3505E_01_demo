from flask import jsonify, request

def users_v2():
    data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]
    return jsonify({
        "version": "v2",
        "users": data
    })
