from flask import current_app, request, jsonify
from bson import ObjectId

# Helper để chuyển ObjectId thành string
def serialize_product(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "description": product.get("description", "")
    }

# 🟢 Tạo sản phẩm
def create_product():
    data = request.get_json()
    db = current_app.db
    result = db.products.insert_one(data)
    product = db.products.find_one({"_id": result.inserted_id})
    return jsonify(serialize_product(product)), 201

# 🔵 Lấy danh sách sản phẩm
def get_products():
    db = current_app.db
    products = [serialize_product(p) for p in db.products.find()]
    return jsonify(products), 200

# 🟡 Lấy sản phẩm theo ID
def get_product_by_id(id):
    db = current_app.db
    product = db.products.find_one({"_id": ObjectId(id)})
    if product:
        return jsonify(serialize_product(product)), 200
    else:
        return jsonify({"message": "Product not found"}), 404

# 🟣 Cập nhật sản phẩm
def update_product(id):
    db = current_app.db
    data = request.get_json()
    result = db.products.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"message": "Product not found"}), 404
    product = db.products.find_one({"_id": ObjectId(id)})
    return jsonify(serialize_product(product)), 200

# 🔴 Xóa sản phẩm
def delete_product(id):
    db = current_app.db
    result = db.products.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"message": "Product not found"}), 404
    return jsonify({"message": "Product deleted"}), 204
