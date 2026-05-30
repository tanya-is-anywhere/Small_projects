def test_create_transaction(client, auth_headers):
    response = client.post('/api/transactions/',
                           json={
                               'type': 'expense',
                               'amount': 500.00,
                               'category': 'Еда',
                               'description': 'Обед'
                           },
                           headers=auth_headers
                           )
    assert response.status_code == 201
    assert response.json['type'] == 'expense'
    assert response.json['amount'] == 500.00


def test_get_transactions(client, auth_headers):
    client.post('/api/transactions/', json={
        'type': 'income', 'amount': 10000, 'category': 'Зарплата'
    }, headers=auth_headers)
    client.post('/api/transactions/', json={
        'type': 'expense', 'amount': 500, 'category': 'Еда'
    }, headers=auth_headers)

    response = client.get('/api/transactions/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 2


def test_update_transaction(client, auth_headers):
    """Обновление транзакции"""
    create_resp = client.post('/api/transactions/', json={
        'type': 'expense', 'amount': 100, 'category': 'Еда'
    }, headers=auth_headers)
    trans_id = create_resp.json['id']

    response = client.put(f'/api/transactions/{trans_id}', json={
        'amount': 200,
        'category': 'Транспорт'
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['amount'] == 200
    assert response.json['category'] == 'Транспорт'


def test_delete_transaction(client, auth_headers):
    create_resp = client.post('/api/transactions/', json={
        'type': 'expense', 'amount': 100, 'category': 'Еда'
    }, headers=auth_headers)
    trans_id = create_resp.json['id']

    response = client.delete(f'/api/transactions/{trans_id}', headers=auth_headers)
    assert response.status_code == 200
    get_resp = client.get('/api/transactions/', headers=auth_headers)
    assert len(get_resp.json) == 0


def test_unauthorized_access(client):
    response = client.get('/api/transactions/')
    assert response.status_code == 401


def test_monthly_report(client, auth_headers):
    client.post('/api/transactions/', json={
        'type': 'income', 'amount': 50000, 'category': 'Зарплата'
    }, headers=auth_headers)
    client.post('/api/transactions/', json={
        'type': 'expense', 'amount': 15000, 'category': 'Еда'
    }, headers=auth_headers)

    from datetime import datetime
    now = datetime.now()

    response = client.get(
        f'/api/transactions/report/{now.year}/{now.month}',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json['total_income'] == 50000
    assert response.json['total_expense'] == 15000
