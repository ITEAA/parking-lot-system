from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # React에서 접근 가능하게 허용

# 차량 저장소 (plate 번호를 key로, 입차 시간 + 경차 여부를 저장)
parked_vehicles = {}  # 예: {'12가1234': {'entry_time': '2025-05-17T14:20:00', 'is_compact': True}}

@app.route("/parked")
def get_parked():
    # 저장된 차량 정보 전체 반환 (경차 여부도 포함)
    return jsonify([
        {
            "plate_number": plate,
            "entry_time": data["entry_time"],
            "is_compact": data["is_compact"]
        }
        for plate, data in parked_vehicles.items()
    ])

@app.route("/entry", methods=["POST"])
def entry():
    data = request.get_json()
    plate = data["plate_number"]
    is_compact = data.get("is_compact", False)  # 프론트에서 전달한 경차 여부 (없으면 False)
    now = datetime.now().isoformat()

    # 차량 정보 저장: 입차 시간 + 경차 여부
    parked_vehicles[plate] = {
        "entry_time": now,
        "is_compact": is_compact
    }

    return jsonify({"status": "입차 완료", "time": now, "is_compact": is_compact})

@app.route("/exit", methods=["POST"])
def exit():
    data = request.get_json()
    plate = data["plate_number"]

    if plate not in parked_vehicles:
        return jsonify({"error": "입차 기록 없음"}), 404

    vehicle_data = parked_vehicles.pop(plate)
    entry_time_str = vehicle_data["entry_time"]
    is_compact = vehicle_data["is_compact"]

    entry_time = datetime.fromisoformat(entry_time_str)
    now = datetime.now()
    minutes = int((now - entry_time).total_seconds() / 60)
    base_fee = minutes * 100  # 기본 요금: 1분당 100원

    # 경차일 경우 요금 50% 할인
    fee = int(base_fee * 0.5) if is_compact else base_fee

    return jsonify({
        "plate_number": plate,
        "fee": fee,
        "parked_minutes": minutes,
        "is_compact": is_compact
    })

if __name__ == "__main__":
    app.run(port=5000)
