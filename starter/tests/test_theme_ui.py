def test_theme_toggle_present(client):
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.data.decode('utf-8')
    assert 'id="theme-toggle"' in data
    assert 'Theme:' in data


def test_theme_css_and_js_match(client):
    # Ensure CSS includes dark-mode selector the JS will toggle
    css = client.get('/static/styles.css')
    assert css.status_code == 200
    css_text = css.data.decode('utf-8')
    assert 'body.dark' in css_text
    # Ensure JS toggles class on body and reads/writes localStorage key
    js = client.get('/static/main.js')
    assert js.status_code == 200
    js_text = js.data.decode('utf-8')
    assert 'document.body.classList' in js_text
    assert 'sudoku_theme' in js_text