from . import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    car_type = db.Column(db.String(20))

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(10), unique=True, nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)

class ParkingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    entry_time = db.Column(db.DateTime)
    exit_time = db.Column(db.DateTime)
    fee = db.Column(db.Float)
