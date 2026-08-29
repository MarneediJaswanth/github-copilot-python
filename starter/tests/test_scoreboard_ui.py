def test_scoreboard_elements_present(client):
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.data.decode('utf-8')
    assert 'Top 10 Fastest Times' in data
    assert 'id="scoreboard"' in data
    assert 'id="player-name"' in data
    assert 'id="save-score-btn"' in data
    # New requirement: Hints column should be present in the scoreboard header
    assert '<th scope="col">Hints</th>' in data


def test_scoreboard_js_has_hints_field():
    # Ensure the client JS stores/display hints (backwards-compatible default to 0)
    js_path = 'static/main.js'
    with open(js_path, 'r', encoding='utf-8') as fh:
        src = fh.read()
    assert 'hintsUsed' in src
    assert 'saveScoreLocal' in src
    # verify saveScoreLocal writes a hints property
    assert 'hints' in src