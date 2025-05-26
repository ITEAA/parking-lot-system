from flask import request, jsonify
from datetime import datetime
from .models import db, Car, ParkingSpot, ParkingRecord

def register_routes(app):
    @app.route("/", methods=["GET"])
    def home():
        return "🚗 Parking Lot System 서버 실행 중!"

    @app.route("/entry", methods=["POST"])
    def entry():
        data = request.get_json()
        plate_number = data.get("plate_number")
        is_compact = data.get("is_compact", False)
        spot_number = data.get("spot_number", "A1")  # 기본값 또는 프론트에서 전달받은 값

        if not plate_number or not spot_number:
            return jsonify({"error": "차량 번호와 주차 공간이 필요합니다."}), 400

        car = Car.query.filter_by(plate_number=plate_number).first()
        if not car:
            car = Car(plate_number=plate_number, is_compact=is_compact)
            db.session.add(car)

        spot = ParkingSpot.query.filter_by(spot_number=spot_number).first()
        if not spot:
            return jsonify({"error": "존재하지 않는 주차 공간입니다."}), 400

        if spot.is_occupied:
            return jsonify({"error": "이미 점유된 주차 공간입니다."}), 400

        spot.is_occupied = True
        record = ParkingRecord(
            car=car,
            spot=spot,
            entry_time=datetime.now()
        )
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

        record = ParkingRecord.query.filter_by(car_id=car.id, exit_time=None).first()
        if not record:
            return jsonify({"error": "입차 기록이 없습니다."}), 404

        record.exit_time = datetime.now()
        duration = (record.exit_time - record.entry_time).total_seconds() / 60
        record.fee = round(duration * 100)  # 분당 100원
        record.spot.is_occupied = False

        db.session.commit()

        return jsonify({
            "message": f"{plate_number} 차량 출차 완료",
            "fee": record.fee,
            "minutes": round(duration)
        }), 200

    @app.route("/parked", methods=["GET"])
    def get_parked():
        parked = ParkingRecord.query.filter_by(exit_time=None).all()
        data = [
            {
                "plate_number": r.car.plate_number,
                "entry_time": r.entry_time.isoformat(),
                "is_compact": r.car.is_compact
            }
            for r in parked
        ]
        return jsonify(data)
