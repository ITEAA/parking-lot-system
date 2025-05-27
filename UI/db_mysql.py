# backend/db_mysql.py
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",          # 또는 127.0.0.1
        user="root",               # 자신의 MySQL 계정
        password="0000",           # MySQL 비밀번호
        database="parking_system", # 위에서 만든 DB 이름
        autocommit=True
    )
