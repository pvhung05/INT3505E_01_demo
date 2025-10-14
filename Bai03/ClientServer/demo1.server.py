from flask import Flask, jsonify, request
app = Flask(__name__)

DATA = {
    "message" : "Hello from REST server",
    "value" : 24
}

@app.route("/api/info", methods=["GET"])
def info():
    return jsonify(DATA)


@app.route("/api/echo", methods=["POST"])
def echo():
    payload = request.json or {}
    return jsonify({"you_sent": payload})
# {
#   "you_sent": {
#     "msg": "Hello REST",
#     "user": "Hung"
#   }
# }

if __name__ == "__main__":
    app.run(port=5001, debug=True)