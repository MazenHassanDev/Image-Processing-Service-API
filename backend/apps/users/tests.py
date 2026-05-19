import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

# Create your tests here.

@pytest.fixture
def client():
    return APIClient()

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