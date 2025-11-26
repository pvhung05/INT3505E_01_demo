from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/api/orders")
def orders():
    version = request.args.get("version")

    if version == "1":
        return jsonify({"version": "1", "orders": ["#A100", "#A200"]})

    if version == "2":
        return jsonify({
            "version": "2",
            "orders": ["#A100", "#A200"],
            "total": 2
        })

    return jsonify({"error": "Missing or unsupported version"}), 400

if __name__ == "__main__":
    app.run(port=3000, debug=True)
