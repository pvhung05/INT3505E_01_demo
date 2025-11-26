from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/api/v1/users")
def users_v1():
    return jsonify({
        "version": "v1",
        "users": ["Alice", "Bob"]
    })

@app.get("/api/v2/users")
def users_v2():
    return jsonify({
        "version": "v2",
        "users": ["Alice", "Bob"],
        "isPremium": True
    })

if __name__ == "__main__":
    app.run(port=3000, debug=True)
