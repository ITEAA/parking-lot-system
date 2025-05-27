from flask import Flask, request, jsonify
from flask_cors import CORS  # 🔹 CORS 모듈 import
from db_mysql_version import create_tables, park_car, exit_car, search_parking_logs, get_current_parking_count, get_all_parking_logs, get_current_parked_cars, MAX_PARKING


app = Flask(__name__)
CORS(app)  # 🔹 모든 요청에 대해 CORS 허용

# DB 테이블이 없다면 생성
create_tables()

@app.route('/api/park', methods=['POST'])
def park():
    data = request.get_json()
    car_number = data.get('car_number')
    car_type = data.get('car_type')
    if not car_number or not car_type:
        return jsonify({"status": "fail", "message": "차량 번호와 차량 종류를 입력하세요."}), 400
    result = park_car(car_number, car_type)
    if result['status'] == 'fail':
        return jsonify(result), 400
    return jsonify(result)

@app.route('/api/exit', methods=['POST'])
def exit_vehicle():
    data = request.get_json()
    car_number = data.get('car_number')
    if not car_number:
        return jsonify({"status": "fail", "message": "차량 번호를 입력하세요."}), 400
    result = exit_car(car_number)
    if result['status'] == 'fail':
        return jsonify(result), 400
    return jsonify(result)

@app.route('/api/logs', methods=['GET'])
def logs():
    car_number = request.args.get('car_number')
    if not car_number:
        return jsonify({"status": "fail", "message": "차량 번호를 입력하세요."}), 400
    logs = search_parking_logs(car_number)
    log_list = [
        {
            "id": log[0],
            "car_number": log[1],
            "car_type": log[2],
            "entry_time": log[3],
            "exit_time": log[4],
            "fee": log[5]
        } for log in logs
    ]
    return jsonify({"status": "success", "logs": log_list})

@app.route('/api/current_count', methods=['GET'])
def current_count():
    count = get_current_parking_count()
    return jsonify({"status": "success", "current_parking_count": count})

@app.route('/api/logs/all', methods=['GET'])
def all_logs():
    logs = get_all_parking_logs()
    log_list = [
        {
            "id": log[0],
            "car_number": log[1],
            "car_type": log[2],
            "entry_time": log[3],
            "exit_time": log[4],
            "fee": log[5]
        } for log in logs
    ]
    return jsonify({"status": "success", "logs": log_list})

@app.route('/api/parking/current', methods=['GET'])
def current_parked_cars():
    cars = get_current_parked_cars()
    car_list = [
        {
            "id": car[0],
            "car_number": car[1],
            "car_type": car[2],
            "entry_time": car[3]
        } for car in cars
    ]
    return jsonify({"status": "success", "cars": car_list})

@app.route('/api/max_capacity')
def get_max_capacity():
    return jsonify({"status": "success", "max_capacity": MAX_PARKING})


if __name__ == '__main__':
    app.run(debug=True)
