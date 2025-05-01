from app import create_app, db
from flask_migrate import Migrate

migrate = Migrate(app, db)

app = create_app()

if __name__ == "__main__":
    app.run()
