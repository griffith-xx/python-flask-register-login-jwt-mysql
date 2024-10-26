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
