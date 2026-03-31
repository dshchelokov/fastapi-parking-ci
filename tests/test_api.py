import pytest
from app.models import Client, Parking, ClientParking
from tests.factories import ClientFactory, ParkingFactory


@pytest.mark.parametrize('path', [
    '/clients', '/parkings'
])
def test_get_methods_200(client, path):
    response = client.get(path)
    assert response.status_code == 200


def test_get_client_not_found(client):
    response = client.get('/clients/999')
    assert response.status_code == 404


def test_create_client(client, db_session):
    data = {'name': 'Дмитрий', 'surname': 'Петров', 'credit_card': '1234', 'car_number': 'AB123CD'}
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    assert response.json['name'] == 'Дмитрий'

    client_obj = Client.query.first()
    assert client_obj is not None
    assert len(Client.query.all()) == 1


def test_create_parking(client, db_session):
    data = {'address': 'улица Центральная 49', 'count_places': 10, 'count_available_places': 5, 'opened': True}
    response = client.post('/parkings', json=data)
    assert response.status_code == 201

    parking = Parking.query.first()
    assert parking.address == 'улица Центральная 49'


@pytest.mark.parking
def test_entry_parking_success(client, db_session):
    client_data = {'name': 'Дмитрий', 'surname': 'Петров', 'credit_card': '1234', 'car_number': 'AB123CD'}
    client.post('/clients', json=client_data)
    parking_data = {'address': 'улица Центральная', 'count_places': 10, 'count_available_places': 5, 'opened': True}
    client.post('/parkings', json=parking_data)

    entry_data = {'client_id': 1, 'parking_id': 1}
    response = client.post('/client_parkings', json=entry_data)
    assert response.status_code == 201

    parking = Parking.query.first()
    assert parking.count_available_places == 4
    client_parking = ClientParking.query.first()
    assert client_parking.time_in is not None


@pytest.mark.parking
def test_exit_parking_success(client, db_session):
    client_data = {'name': 'Дмитрий', 'surname': 'Петров', 'credit_card': '1234', 'car_number': 'AB123CD'}
    client.post('/clients', json=client_data)
    parking_data = {'address': 'улица Центральная', 'count_places': 10, 'count_available_places': 5, 'opened': True}
    client.post('/parkings', json=parking_data)
    client.post('/client_parkings', json={'client_id': 1, 'parking_id': 1})

    response = client.delete('/client_parkings', json={'client_id': 1, 'parking_id': 1})
    assert response.status_code == 200

    client_parking = ClientParking.query.first()
    assert client_parking.time_out is not None
    assert client_parking.time_out > client_parking.time_in
    parking = Parking.query.first()
    assert parking.count_available_places == 5


def test_create_client_factory(db_session):
    client = ClientFactory.create()
    assert client.id is not None
    assert len(Client.query.all()) == 1


def test_create_parking_factory(db_session):
    parking = ParkingFactory.create()
    assert parking.id is not None
    assert parking.count_available_places == parking.count_places
    assert len(Parking.query.all()) == 1
