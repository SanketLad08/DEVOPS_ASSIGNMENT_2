import pytest
from app.ACEest_fitness_app import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'UP'

def test_version_default(client):
    rv = client.get('/version')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'version' in data

def test_list_classes(client):
    rv = client.get('/api/classes')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'classes' in data and isinstance(data['classes'], list)

def test_add_member_valid(client):
    payload = {'name': 'Test User', 'age': 28}
    rv = client.post('/api/members', json=payload)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['member']['name'] == 'Test User'

def test_add_member_invalid(client):
    payload = {'name': '', 'age': 'not-int'}
    rv = client.post('/api/members', json=payload)
    assert rv.status_code == 400

def test_get_schedules(client):
    rv = client.get('/api/schedules')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'schedules' in data
