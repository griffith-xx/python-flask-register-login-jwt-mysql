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