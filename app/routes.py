from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return 'Hello, Parking Lot System!'

@bp.route('/cars')
def get_cars():
    from app.models import Car
    cars = Car.query.all()
    return jsonify([{'id': c.id, 'number': c.number, 'car_type': c.car_type} for c in cars])
