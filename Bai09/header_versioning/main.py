from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/api/users")
def get_users():
    version = request.headers.get("X-API-Version")

    if version == "1":
        return jsonify({"version": "1",
                         "users": ["Alice", "Bob"]})

    if version == "2":
        return jsonify({
            "version": "2",
            "users": ["Alice", "Bob"],
            "count": 2
        })

    return jsonify({"error": "Version not supported"}), 400

if __name__ == "__main__":
    app.run(port=3000, debug=True)
