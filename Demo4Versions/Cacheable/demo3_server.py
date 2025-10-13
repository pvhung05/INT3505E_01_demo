from flask import Flask, jsonify, request, make_response
import hashlib
import time

app = Flask(__name__)

# resource state (thay đổi khi bạn gọi /update)
DATA = {"value": "initial"}
LAST_MODIFIED = time.time()

def compute_etag(obj):
    s = repr(obj).encode("utf-8")
    return hashlib.sha1(s).hexdigest()

@app.route("/api/data", methods=["GET"])
def get_data():
    etag = compute_etag(DATA)
    # trả header Cache-Control để cho client/proxy biết có thể cache trong 30s
    resp = make_response(jsonify(DATA))
    resp.headers["Cache-Control"] = "public, max-age=30"
    resp.headers["ETag"] = etag

    # If client sends If-None-Match, so we can short-circuit with 304
    inm = request.headers.get("If-None-Match")
    if inm and inm == etag:
        # không gửi body => 304
        r = make_response("", 304)
        r.headers["ETag"] = etag
        r.headers["Cache-Control"] = "public, max-age=30"
        return r

    return resp

@app.route("/api/update", methods=["POST"])
def update():
    new = request.json or {}
    DATA.update(new)
    global LAST_MODIFIED
    LAST_MODIFIED = time.time()
    return jsonify({"status": "ok", "data": DATA})

if __name__ == "__main__":
    app.run(port=5003, debug=True)
