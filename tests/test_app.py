import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from app import app, init_db, PROGRAMS

@pytest.fixture
def client():
    import tempfile
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['DB_PATH'] = db_path
    app.config['TESTING'] = True
    with app.test_client() as c:
        init_db()
        yield c
    os.environ.pop('DB_PATH')
    os.close(db_fd)
    os.unlink(db_path)

# ── Health Tests ──────────────────────
def test_health_returns_200(client):
    r = client.get('/health')
    assert r.status_code == 200

def test_health_contains_status(client):
    r = client.get('/health')
    data = r.get_json()
    assert data['status'] == 'healthy'

# ── Program Tests ─────────────────────
def test_programs_returns_three(client):
    r = client.get('/programs')
    data = r.get_json()
    assert len(data) == 3

def test_fat_loss_in_programs(client):
    r = client.get('/programs')
    data = r.get_json()
    assert 'Fat Loss' in data

# ── Client Tests ──────────────────────
def test_add_client_returns_201(client):
    r = client.post('/clients',
        json={'name':'Arjun','age':25,
              'weight':70,'program':'Fat Loss'})
    assert r.status_code == 201

def test_calorie_calculation(client):
    r = client.post('/clients',
        json={'name':'Ravi','age':22,
              'weight':70,'program':'Fat Loss'})
    data = r.get_json()
    assert data['calories'] == 1540

def test_duplicate_client_returns_409(client):
    client.post('/clients',
        json={'name':'Same','age':25,
              'weight':70,'program':'Fat Loss'})
    r = client.post('/clients',
        json={'name':'Same','age':25,
              'weight':70,'program':'Fat Loss'})
    assert r.status_code == 409

def test_missing_name_returns_400(client):
    r = client.post('/clients',
        json={'age':25,'weight':70,
              'program':'Fat Loss'})
    assert r.status_code == 400

def test_invalid_program_returns_400(client):
    r = client.post('/clients',
        json={'name':'Test','age':25,
              'weight':70,'program':'Unknown'})
    assert r.status_code == 400

def test_get_clients_returns_list(client):
    r = client.get('/clients')
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

# ── Business Logic Tests ──────────────
def test_fat_loss_calorie_factor():
    assert PROGRAMS['Fat Loss']['calorie_factor'] == 22

def test_muscle_gain_calorie_factor():
    assert PROGRAMS['Muscle Gain']['calorie_factor'] == 35

def test_beginner_calorie_factor():
    assert PROGRAMS['Beginner']['calorie_factor'] == 26