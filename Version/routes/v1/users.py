from flask import jsonify, request

def users_v1():
    data = [
        {"id": 1, "name": "Alice (v1)"},
        {"id": 2, "name": "Bob (v1)"}
    ]
    return jsonify({
        "version": "v1",
        "users": data
    })
