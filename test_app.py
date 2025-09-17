import pytest
from app import app
import os


@pytest.fixture
def client():
    # Временно меняем файл хранения для тестов
    app.config['TESTING'] = True
    app.config['QUOTES_FILE'] = 'test_quotes.json'

    with app.test_client() as client:
        yield client

    # Удаляем тестовый файл после завершения
    if os.path.exists('test_quotes.json'):
        os.remove('test_quotes.json')


def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    # Используем decode() для преобразования байтов в строку
    assert "Цитата дня" in response.data.decode('utf-8')


def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    # Проверяем только наличие поля status, игнорируя поле time
    assert 'status' in response.json
    assert response.json['status'] == 'OK'


def test_add_quote_form(client):
    response = client.get('/add')
    assert response.status_code == 200
    # Используем decode() для преобразования байтов в строку
    assert "Добавить новую цитату" in response.data.decode('utf-8')


def test_api_random_quote(client):
    response = client.get('/api/quote')
    assert response.status_code == 200
    assert 'text' in response.json
    assert 'author' in response.json


def test_api_add_quote(client):
    # Тестируем добавление через API
    response = client.post('/api/quote',
                           json={'text': 'Test quote', 'author': 'Test Author'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    # Проверяем, что цитата действительно добавилась
    response = client.get('/api/quote')
    assert response.status_code == 200
    assert 'test quote' in response.json['text']
