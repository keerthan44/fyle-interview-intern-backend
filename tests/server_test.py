def test_server_ready(client):
    response = client.get('/')

    assert response.status_code == 200

def test_server_http_exception(client):
    response = client.get('/create')

    assert response.status_code == 404
