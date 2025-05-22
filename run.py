from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


# 📁 파일: app/__init__.py
from flask import Flask
from .routes import register_routes
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # DB 연결 설정
    app.config['DB_CONFIG'] = {
        'host': os.getenv("DB_HOST", "localhost"),
        'port': int(os.getenv("DB_PORT", 3306)),
        'user': os.getenv("DB_USER", "root"),
        'password': os.getenv("DB_PASSWORD"),
        'database': os.getenv("DB_NAME", "testdb")
    }

    # 라우트 등록
    register_routes(app)

    return app


# 📁 파일: app/routes.py
from flask import request, jsonify
import mysql.connector

# 라우트 함수 분리 등록

def register_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return "🚗 Parking Lot System 서버 실행 중!"

    @app.route("/entry", methods=["POST"])
    def entry():
        data = request.get_json()
        car_number = data.get("car_number")

        db = mysql.connector.connect(**app.config['DB_CONFIG'])
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO parking_log (car_number, entry_time)
            VALUES (%s, NOW())
        """, (car_number,))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"message": f"{car_number} 입차 완료"}), 200

    @app.route("/exit", methods=["POST"])
    def exit():
        data = request.get_json()
        car_number = data.get("car_number")

        db = mysql.connector.connect(**app.config['DB_CONFIG'])
        cursor = db.cursor()
        cursor.execute("""
            UPDATE parking_log
            SET exit_time = NOW()
            WHERE car_number = %s AND exit_time IS NULL
        """, (car_number,))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"message": f"{car_number} 출차 완료"}), 200
