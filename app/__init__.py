from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import register_routes
import os
from dotenv import load_dotenv
from .db import db

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # ✅ 여기에 테이블 생성 코드 추가
    with app.app_context():
        db.create_all()

    register_routes(app)

    return app
