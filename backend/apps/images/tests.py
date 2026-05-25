import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PillowImage
import io
from unittest.mock import patch

# Create your tests here.
class LargeSimpleUploadedFile(SimpleUploadedFile):
    @property
    def size(self):
        return 11 * 1024 * 1024
    
    @size.setter
    def size(self, value):
        pass

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")

@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client

def create_dummy_image(format='JPEG'):
    img = PillowImage.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return SimpleUploadedFile(
        f"test.{format.lower()}",
        buffer.read(),
        content_type=f"image/{format.lower()}"
    )

def test_upload_success(auth_client):
    response = auth_client.post(reverse('list_create_view'), {
        "file": create_dummy_image()
    }, format='multipart')

    assert response.status_code == 201

@pytest.mark.django_db
def test_upload_unauthenticated(client):
    response = client.post(reverse('list_create_view'), {
        "file": create_dummy_image()
    }, format='multipart')

    assert response.status_code == 401

def test_upload_file_too_large():
    image = create_dummy_image()
    large_image = LargeSimpleUploadedFile(
        image.name,
        image.read(),
        image.content_type
    )

    from apps.images.serializers import ImageUploadSerializer
    serializer = ImageUploadSerializer(data={"file": large_image})
    assert serializer.is_valid() == False
    assert 'file' in serializer.errors

def test_upload_invalid_file():
    invalid_image = SimpleUploadedFile(
        'test.jpg',
        b"This is not an image, plain text.",
        content_type="image/jpeg"
    )

    from apps.images.serializers import ImageUploadSerializer
    serializer = ImageUploadSerializer(data={"file": invalid_image})
    assert serializer.is_valid() == False
    assert 'file' in serializer.errors

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PillowImage
import io
from unittest.mock import patch

# Create your tests here.
class LargeSimpleUploadedFile(SimpleUploadedFile):
    @property
    def size(self):
        return 11 * 1024 * 1024
    
    @size.setter
    def size(self, value):
        pass

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")

@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client

def create_dummy_image(format='JPEG'):
    img = PillowImage.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return SimpleUploadedFile(
        f"test.{format.lower()}",
        buffer.read(),
        content_type=f"image/{format.lower()}"
    )

def test_upload_success(auth_client):
    response = auth_client.post(reverse('list_create_view'), {
        "file": create_dummy_image()
    }, format='multipart')

    assert response.status_code == 201

@pytest.mark.django_db
def test_upload_unauthenticated(client):
    response = client.post(reverse('list_create_view'), {
        "file": create_dummy_image()
    }, format='multipart')

    assert response.status_code == 401

def test_upload_file_too_large():
    image = create_dummy_image()
    large_image = LargeSimpleUploadedFile(
        image.name,
        image.read(),
        image.content_type
    )

    from apps.images.serializers import ImageUploadSerializer
    serializer = ImageUploadSerializer(data={"file": large_image})
    assert serializer.is_valid() == False
    assert 'file' in serializer.errors

def test_upload_invalid_file():
    invalid_image = SimpleUploadedFile(
        'test.jpg',
        b"This is not an image, plain text.",
        content_type="image/jpeg"
    )

    from apps.images.serializers import ImageUploadSerializer
    serializer = ImageUploadSerializer(data={"file": invalid_image})
    assert serializer.is_valid() == False
    assert 'file' in serializer.errors

def test_unsupported_format():
    img = PillowImage.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='ICO')
    buffer.seek(0)
    invalid_file = SimpleUploadedFile(
        'test.ico',
        buffer.read(),
        content_type='image/x-icon'
    )
    
    from apps.images.serializers import ImageUploadSerializer
    serializer = ImageUploadSerializer(data={"file": invalid_file})
    assert serializer.is_valid() == False
    assert 'file' in serializer.errors