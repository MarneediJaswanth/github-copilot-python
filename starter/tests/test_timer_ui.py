def test_index_contains_timer(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'id="timer"' in resp.data