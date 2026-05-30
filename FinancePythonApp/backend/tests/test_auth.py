def test_register_success(client):
    """Успешная регистрация"""
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'password': 'secret123'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created'


def test_register_duplicate(client):
    """Регистрация с существующим именем"""
    # Первая регистрация — успешна
    client.post('/api/auth/register', json={
        'username': 'duplicate',
        'password': 'secret123'
    })

    # Вторая регистрация с тем же именем — должна вернуть ошибку
    response = client.post('/api/auth/register', json={
        'username': 'duplicate',
        'password': 'secret123'
    })

    assert response.status_code != 201
    assert response.status_code in [400, 409, 422]


def test_login_success(client):
    """Успешный вход"""
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'password': 'mypassword'
    })
    response = client.post('/api/auth/login', json={
        'username': 'loginuser',
        'password': 'mypassword'
    })
    assert response.status_code == 200
    assert 'token' in response.json


def test_login_wrong_password(client):
    """Вход с неверным паролем"""
    client.post('/api/auth/register', json={
        'username': 'wrongpw',
        'password': 'correct'
    })
    response = client.post('/api/auth/login', json={
        'username': 'wrongpw',
        'password': 'wrong_password'
    })
    assert response.status_code == 401
