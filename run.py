from app import db, create_app

app = create_app()

# ✅ 아래 코드 임시 추가 (처음 1회만 필요)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
