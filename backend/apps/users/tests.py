import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

# Create your tests here.

@pytest.fixture
def client():
    return APIClient()


# Register Tests

@pytest.mark.django_db
def test_register_success(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }, format='json')

    assert response.status_code == 201
    assert response.data['user']['username'] == 'testuser'
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_register_duplicate_username(client):
    User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'email': 'other@example.com',
        'password': 'testpassword123'
    }, format='json')

    assert response.status_code == 400

@pytest.mark.django_db
def test_register_duplicate_email(client):
    User.objects.create_user(username= "testuser", email="test@example.com", password="testpassword123")
    response = client.post(reverse('register'), {
        'username': 'otheruser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }, format='json')

    assert response.status_code == 400

@pytest.mark.django_db
def test_register_missing_fields(client):
    response = client.post(reverse('register'), {
        'email': 'test@example.com',
        'password': 'testpassword123'
    }, format='json')

    assert response.status_code == 400


# Login Tests
@pytest.mark.django_db
def test_login_success(client):
    User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'testpassword123'
    }, format='json')

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_login_wrong_password(client):
    User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'wrongpassword123'
    }, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
def test_login_nonexistent_user(client):
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'wrongpassword123'
    }, format='json')

    assert response.status_code == 401


# Logout Tests
@pytest.mark.django_db
def test_logout_success(client):
    User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
    login_response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'testpassword123'
    }, format='json')

    refresh_token = login_response.data['refresh']
    response = client.post(reverse('logout'), {
        'refresh': refresh_token
    }, format='json')

    assert response.status_code == 200




