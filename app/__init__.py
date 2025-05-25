from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from .models import db, Car, ParkingSpot, ParkingRecord  # models에서 정의된 db import
from .routes import register_routes

# .env 로드
load_dotenv()

def create_app():
    app = Flask(__name__)

    # DB 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # DB & Migrate 초기화
    db.init_app(app)
    Migrate(app, db)

    # 테이블 자동 생성
    with app.app_context():
        db.create_all()

    # 라우트 등록
    register_routes(app)

    return app
