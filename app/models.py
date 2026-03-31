from app import database
from datetime import datetime
from sqlalchemy.orm import relationship


class Client(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)
    surname = database.Column(database.String(50), nullable=False)
    credit_card = database.Column(database.String(50))
    car_number = database.Column(database.String(10))

    parkings = relationship('ClientParking', back_populates='client', uselist=True)


class Parking(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    address = database.Column(database.String(100), nullable=False)
    opened = database.Column(database.Boolean, default=False)
    count_places = database.Column(database.Integer, nullable=False)
    count_available_places = database.Column(database.Integer, nullable=False)

    parkings = relationship('ClientParking', back_populates='parking', uselist=True)


class ClientParking(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    client_id = database.Column(database.Integer, database.ForeignKey('client.id'), nullable=False)
    parking_id = database.Column(database.Integer, database.ForeignKey('parking.id'), nullable=False)
    time_in = database.Column(database.DateTime)
    time_out = database.Column(database.DateTime)

    client = relationship('Client', back_populates='parkings')
    parking = relationship('Parking', back_populates='parkings')

    __table_args__ = (database.UniqueConstraint('client_id', 'parking_id'),)
