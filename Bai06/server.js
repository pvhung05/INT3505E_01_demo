require("dotenv").config();
const express = require("express");
const jwt = require("jsonwebtoken");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

// Giả lập user trong DB
const users = [
  { id: 1, username: "admin", password: "123456" },
  { id: 2, username: "hung", password: "abcd" },
];

// Route login -> tạo token
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  const user = users.find(
    (u) => u.username === username && u.password === password
  );

  if (!user) return res.status(401).json({ message: "Sai username hoặc password!" });

  // Tạo JWT
  const token = jwt.sign(
    { id: user.id, username: user.username },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRES_IN }
  );

  res.json({ message: "Đăng nhập thành công!", token });
});

// Middleware kiểm tra JWT
function verifyToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1]; // "Bearer <token>"

  if (!token) return res.status(403).json({ message: "Thiếu token!" });

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.status(401).json({ message: "Token không hợp lệ!" });
    req.user = user;
    next();
  });
}

// Route bảo vệ - chỉ truy cập nếu có JWT hợp lệ
app.get("/profile", verifyToken, (req, res) => {
  res.json({
    message: "Thông tin người dùng",
    user: req.user,
  });
});

app.listen(3000, () => console.log("✅ Server chạy tại http://localhost:3000"));
