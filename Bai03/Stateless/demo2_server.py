from flask import Flask, jsonify, request, abort
import jwt
import datetime

app = Flask(__name__)
SECRET = "abc-pham-van-hung"

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    if not username:
        abort(400, "need username")
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return jsonify({"token": token})

# {"username":"hung"}

@app.route("/api/protected", methods=["GET"])
def protected():
    auth = request.headers.get("Author", "")
    if not auth.startswith("Bearer "):
        abort(401)
    token = auth.split(" ", 1)[1]
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
    except Exception as e:
        abort(401, str(e))
    return jsonify({"message": f"Hello {data['sub']}, this is stateless!"})


# Key: Author
# Value: Bearer <token>

if __name__ == "__main__":
    app.run(port=5002, debug=True)

