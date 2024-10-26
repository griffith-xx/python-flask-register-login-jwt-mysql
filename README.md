# ระบบลงทะเบียนและเข้าสู่ระบบด้วย Flask, JWT และ MySQL

โปรเจกต์นี้เป็นตัวอย่างระบบลงทะเบียนผู้ใช้และเข้าสู่ระบบ โดยใช้ Flask สำหรับ Backend, JWT (JSON Web Token) สำหรับการยืนยันตัวตน และ MySQL ในการจัดเก็บข้อมูลผู้ใช้

## ฟีเจอร์
- ลงทะเบียนผู้ใช้: บันทึกข้อมูลผู้ใช้ใหม่ด้วยชื่อผู้ใช้ อีเมล และรหัสผ่าน
- เข้าสู่ระบบ: ตรวจสอบข้อมูลผู้ใช้ และส่งคืน JWT Token
- บันทึกข้อมูลใน MySQL: เก็บข้อมูลผู้ใช้ในฐานข้อมูล MySQL
- การแฮชรหัสผ่าน: ปกป้องรหัสผ่านด้วยการแฮช (bcrypt)

## สิ่งที่ต้องมี
- Python 3.x
- MySQL Server
- pip (ตัวจัดการแพ็กเกจของ Python)

## การติดตั้ง
1. **โคลนโปรเจกต์นี้:**
```
git clone https://github.com/griffith-xx/python-flask-register-login-jwt-mysql
cd python-flask-register-login-jwt-mysql
```

2. **สร้าง Virtual Environment:**
```
python -m venv venv
.\venv\Scripts\activate
```

3. **ติดตั้ง Dependencies:**
```
pip install -r requirements.txt
```

4. **กำหนด Environment ในไฟล์ .env**
```
MYSQL_HOST=your_host
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database
SECRET_KEY=your_secret_key
```

5. **สร้าง Models**
โมเดล users ที่มี id user email และ password
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
```

6. **สร้าง Routes**
สร้าง route สองเส้น register สำหรับบันถึก user ลง database และ login เพื่อทำการส่ง jwt กลับไปคืนไปให้ frontend
```python
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User

routes_bp = Blueprint("route", __name__)

@routes_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    if (
        User.query.filter_by(username=username).first()
        or User.query.filter_by(email=email).first()
    ):
        return jsonify({"msg": "Username or email already exists"}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully!"}), 201


@routes_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401
```
7. **สร้าง App**
import routes มา register ลง ใน app
```python
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, SECRET_KEY
from routes import routes_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)
app.config["JWT_SECRET_KEY"] = SECRET_KEY

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(routes_bp)

@app.before_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
```

8. **รัน App**
```python
python app.py
```

**ตัวอย่าง request register**
```
{
  "email": "johndoe@gmail.com",
  "password": "johndoe123456",
  "username": "johndoe"
}
```

**ตัวอย่าง request login**
```
{
  "email": "johndoe@gmail.com",
  "password": "johndoe123456",
}
```