import pytest
import app as sudoku_app_module


@pytest.fixture
def client():
    sudoku_app_module.app.config['TESTING'] = True
    with sudoku_app_module.app.test_client() as client:
        yield client
