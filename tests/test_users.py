from app import schemas
import pytest
from jose import jwt
from app.config import settings

# def test_root(client):
#     res = client.get('/')
#     print(res.json())
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'sample@gmail.com', 'password': 'sample123'})
    new_user = schemas.User(**res.json())
    assert new_user.email == 'sample@gmail.com'
    assert res.status_code == 201


def test_login(client, test_user):
    res = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert res.status_code == 200


@pytest.mark.parametrize("username,password,status_code", [
    ('wrong@gmail.com', 'sample123', 404),
    ('sample@gmail.com', 'wrong', 404),
    (None, 'password', 422)
])
def test_incorrect_login(client, test_user,username,password,status_code):
    res = client.post(
        '/login', data={'username': username, 'password': password})
    assert res.status_code == status_code
