def test_scoreboard_elements_present(client):
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.data.decode('utf-8')
    assert 'Top 10 Fastest Times' in data
    assert 'id="scoreboard"' in data
    assert 'id="player-name"' in data
    assert 'id="save-score-btn"' in data