from flask import request, jsonify
from .models import db, Car, ParkingSpot, ParkingRecord
from datetime import datetime


def register_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return "🚗 Parking Lot System 서버 실행 중!"

    @app.route("/entry", methods=["POST"])
    def entry():
        data = request.get_json()
        plate_number = data.get("plate_number")
        car_type = data.get("car_type")
        spot_number = data.get("spot_number")

        car = Car.query.filter_by(plate_number=plate_number).first()
        if not car:
            car = Car(plate_number=plate_number, car_type=car_type)
            db.session.add(car)

        spot = ParkingSpot.query.filter_by(spot_number=spot_number).first()
        if not spot:
            return jsonify({"error": "존재하지 않는 주차 공간입니다."}), 400

        if spot.is_occupied:
            return jsonify({"error": "이미 점유된 주차 공간입니다."}), 400

        spot.is_occupied = True
        record = ParkingRecord(car=car, spot=spot, entry_time=datetime.now())
        db.session.add(record)
        db.session.commit()

        return jsonify({"message": f"{plate_number} 차량 입차 완료"}), 200

    @app.route("/exit", methods=["POST"])
    def exit():
        data = request.get_json()
        plate_number = data.get("plate_number")

        car = Car.query.filter_by(plate_number=plate_number).first()
        if not car:
            return jsonify({"error": "차량 정보가 없습니다."}), 404

        record = ParkingRecord.query.filter_by(car=car, exit_time=None).first()
        if not record:
            return jsonify({"error": "입차 기록이 없습니다."}), 404

        record.exit_time = datetime.now()
        duration = (record.exit_time - record.entry_time).total_seconds() / 60
        record.fee = round(duration * 100)  # 분당 100원
        record.spot.is_occupied = False

        db.session.commit()

        return jsonify({
            "message": f"{plate_number} 차량 출차 완료",
            "fee": record.fee
        }), 200
