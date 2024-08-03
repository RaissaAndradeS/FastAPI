from http import HTTPStatus

from fastapi.testeclient import TesteClient

from fast_zero.app import app

client = TesteClient(app)


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TesteClient(app)  # Organização (Arrange)

    response = client.get('/')  # Ação (Act)

    assert response.status_code == HTTPStatus.OK  # Afirmando (Assert)
    assert response.json() == {'message': 'Olá mundo'}