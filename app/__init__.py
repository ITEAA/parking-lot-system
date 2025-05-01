from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    db.init_app(app)
    migrate.init_app(app, db)
    from app import routes
    app.register_blueprint(routes.bp)
    return app
