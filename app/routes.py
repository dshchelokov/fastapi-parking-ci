from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from app import db
from app.models import Client, ClientParking, Parking

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return jsonify(
        [
            {
                "id": client.id,
                "name": client.name,
                "surname": client.surname,
                "credit_card": client.credit_card,
                "car_number": client.car_number,
            }
            for client in clients
        ]
    )


@api_blueprint.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(
        {
            "id": client.id,
            "name": client.name,
            "surname": client.surname,
            "credit_card": client.credit_card,
            "car_number": client.car_number,
        }
    )


@api_blueprint.route("/clients", methods=["POST"])
def create_client():
    data = request.get_json()
    client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data.get("credit_card"),
        car_number=data.get("car_number"),
    )
    db.session.add(client)
    db.session.commit()
    return (
        jsonify({"id": client.id, "name": client.name, "surname": client.surname}),
        201,
    )


@api_blueprint.route("/parkings", methods=["GET", "POST"])
def parkings():
    if request.method == "GET":
        parkings_list = Parking.query.all()
        return jsonify(
            [
                {
                    "id": p.id,
                    "address": p.address,
                    "opened": p.opened,
                    "count_places": p.count_places,
                    "count_available_places": p.count_available_places,
                }
                for p in parkings_list
            ]
        )
    elif request.method == "POST":
        data = request.get_json()
        parking = Parking(
            address=data["address"],
            opened=data.get("opened", False),
            count_places=data["count_places"],
            count_available_places=data["count_available_places"],
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify({"id": parking.id, "address": parking.address}), 201


@api_blueprint.route("/client_parkings", methods=["POST"])
def entry_parking():
    data = request.get_json()
    client = Client.query.get_or_404(data["client_id"])
    parking = Parking.query.get_or_404(data["parking_id"])

    if not parking.opened:
        return jsonify({"error": "Parking is closed"}), 400
    if parking.count_available_places <= 0:
        return jsonify({"error": "No available places"}), 400

    existing = ClientParking.query.filter_by(
        client_id=client.id, parking_id=parking.id
    ).first()
    if existing:
        return jsonify({"error": "Client already parked"}), 400

    parking.count_available_places -= 1
    client_parking = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        time_in=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db.session.add(client_parking)
    db.session.commit()
    return jsonify({"message": "Entry logged"}), 201


@api_blueprint.route("/client_parkings", methods=["DELETE"])
def exit_parking():
    data = request.get_json()
    client = Client.query.get_or_404(data["client_id"])
    parking = Parking.query.get_or_404(data["parking_id"])

    client_parking = ClientParking.query.filter_by(
        client_id=client.id, parking_id=parking.id
    ).first_or_404()
    if not client_parking.time_in:
        return jsonify({"error": "No entry record"}), 400
    if client_parking.time_out:
        return jsonify({"error": "Already exited"}), 400
    if not client.credit_card:
        return jsonify({"error": "No credit card attached"}), 400

    client_parking.time_out = datetime.now(timezone.utc).replace(tzinfo=None)
    if client_parking.time_out <= client_parking.time_in:
        return jsonify({"error": "Invalid exit time"}), 400

    parking.count_available_places += 1
    db.session.commit()
    return jsonify({"message": "Exit logged and paid"})
