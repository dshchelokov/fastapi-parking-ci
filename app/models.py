from app import db


class Client(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    credit_card = db.Column(db.String(16))
    car_number = db.Column(db.String(16))


class Parking(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), nullable=False)
    opened = db.Column(db.Boolean, default=False)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)


class ClientParking(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=False)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
