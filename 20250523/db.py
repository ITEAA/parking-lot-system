import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'parking.db')

MAX_PARKING = 100

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_number TEXT NOT NULL UNIQUE,
        car_type TEXT NOT NULL,
        entry_time DATETIME DEFAULT (datetime('now', 'localtime'))
    );''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parking_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_number TEXT NOT NULL,
        car_type TEXT NOT NULL,
        entry_time DATETIME NOT NULL,
        exit_time DATETIME NOT NULL,
        fee INTEGER NOT NULL
    );''')
    conn.commit()
    conn.close()

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
    cursor.execute("SELECT 1 FROM parking WHERE car_number = ?", (car_number,))
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
        cursor.execute("INSERT INTO parking (car_number, car_type) VALUES (?, ?)", (car_number, car_type))
        conn.commit()
        return {"status": "success", "message": "입차 완료"}
    finally:
        conn.close()

def calculate_fee(entry_time_str, exit_time, car_type):
    try:
        entry_time = datetime.strptime(entry_time_str, '%Y-%m-%d %H:%M:%S')
    except:
        entry_time = datetime.strptime(entry_time_str, '%Y-%m-%d %H:%M:%S.%f')
    duration = (exit_time - entry_time).total_seconds() // 60
    if duration <= 5:
        return 0
    fee = 100 * int(duration) if car_type in ['SUV', '승용차'] else 50 * int(duration)
    return int(fee)

def exit_car(car_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT car_type, entry_time FROM parking WHERE car_number = ?", (car_number,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return {"status": "fail", "message": "입차된 차량이 아닙니다."}
    car_type, entry_time_str = result
    exit_time = datetime.now()
    fee = calculate_fee(entry_time_str, exit_time, car_type)
    cursor.execute("INSERT INTO parking_log (car_number, car_type, entry_time, exit_time, fee) VALUES (?, ?, ?, ?, ?)",
                   (car_number, car_type, entry_time_str, exit_time.strftime('%Y-%m-%d %H:%M:%S'), fee))
    cursor.execute("DELETE FROM parking WHERE car_number = ?", (car_number,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"출차 완료, 요금: {fee}원"}

def search_parking_logs(car_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking_log WHERE car_number = ?", (car_number,))
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_all_parking_logs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parking_log ORDER BY entry_time DESC')
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_current_parked_cars():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parking ORDER BY entry_time DESC')
    cars = cursor.fetchall()
    conn.close()
    return cars

