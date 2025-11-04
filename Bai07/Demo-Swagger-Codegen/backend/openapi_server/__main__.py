import connexion
from pymongo import MongoClient
from flask_cors import CORS
from openapi_server import encoder

def main():
    # Khởi tạo ứng dụng Connexion (tích hợp Flask)
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'Product API'}, pythonic_params=True)

    # Cho phép CORS
    CORS(app.app)

    # 🔗 Kết nối MongoDB Atlas
    # ⚠️ THAY <password> BẰNG MẬT KHẨU THẬT CỦA USER TRONG CLUSTER
    uri = "mongodb+srv://23021569_db_user:MsAUtaWUpUAXeFrN@demo-mongodb.mnednop.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)

    # Truy cập database (MongoDB sẽ tự tạo nếu chưa có)
    db = client["productdb"]
    app.app.db = db

    # Chạy server Flask tích hợp
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()
