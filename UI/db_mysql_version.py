# backend/db_mysql_version.py
from datetime import datetime
from db_mysql import connect_db

MAX_PARKING = 5

def get_current_parking_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM parking;")
    n = cursor.fetchone()[0]
    conn.close()
    return n

def is_car_parked(car_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM parking WHERE car_number = %s", (car_number,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def park_car(car_number, car_type):
    if get_current_parking_count() >= MAX_PARKING:
        return {"status": "fail", "message": "만차입니다."}
    if is_car_parked(car_number):
        return {"status": "fail", "message": "이미 입차된 차량입니다."}
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO parking (car_number, car_type) VALUES (%s, %s)",
            (car_number, car_type)
        )
        return {"status": "success", "message": "입차 완료"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}
    finally:
        conn.close()

def calculate_fee(entry_time_str, exit_time, car_type):
    entry_time = datetime.strptime(entry_time_str, '%Y-%m-%d %H:%M:%S')
    duration = int((exit_time - entry_time).total_seconds() // 60)

    if duration <= 5:
        return 0

    # 기본 요금
    if car_type == '경차':
        fee = 2000
    else:  # 승용차, SUV, 기타
        fee = 3000

    # 5분 초과 후 30분 단위로 1000원씩 추가
    extra_minutes = duration - 5
    if extra_minutes > 30:
        extra_units = (extra_minutes - 1) // 30  # 35~65분: 1, 65~95분: 2, ...
        fee += extra_units * 1000

    return fee


def exit_car(car_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT car_type, entry_time FROM parking WHERE car_number = %s", (car_number,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return {"status": "fail", "message": "입차된 차량이 아닙니다."}
    car_type, entry_time = result
    exit_time = datetime.now()
    fee = calculate_fee(entry_time.strftime('%Y-%m-%d %H:%M:%S'), exit_time, car_type)
    cursor.execute(
        "INSERT INTO parking_log (car_number, car_type, entry_time, exit_time, fee) VALUES (%s, %s, %s, %s, %s)",
        (car_number, car_type, entry_time, exit_time, fee)
    )
    cursor.execute("DELETE FROM parking WHERE car_number = %s", (car_number,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"출차 완료, 요금: {fee}원"}

def search_parking_logs(car_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking_log WHERE car_number = %s", (car_number,))
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_all_parking_logs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking_log ORDER BY entry_time DESC")
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_current_parked_cars():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking ORDER BY entry_time DESC")
    cars = cursor.fetchall()
    conn.close()
    return cars

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking (
            id INT AUTO_INCREMENT PRIMARY KEY,
            car_number VARCHAR(20) NOT NULL,
            car_type VARCHAR(20) NOT NULL,
            entry_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            car_number VARCHAR(20) NOT NULL,
            car_type VARCHAR(20) NOT NULL,
            entry_time DATETIME NOT NULL,
            exit_time DATETIME NOT NULL,
            fee INT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

