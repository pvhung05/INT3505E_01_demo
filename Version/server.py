from flask import Flask, request, jsonify
from routes.v1.users import users_v1
from routes.v2.users import users_v2

app = Flask(__name__)

# Middleware JSON tự động
@app.before_request
def before_request_func():
    if request.is_json:
        request.get_json(silent=True)

# Route versioning giống Express: /api/:version/users
@app.route("/api/<version>/users", methods=["GET"])
def handle_users(version):
    if version == "v1":
        return users_v1()
    elif version == "v2":
        return users_v2()
    else:
        return jsonify({"error": "Version not supported"}), 404

# Chạy server
if __name__ == "__main__":
    PORT = 3000
    print(f"🚀 Server running on http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
