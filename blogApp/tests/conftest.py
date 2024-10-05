import pytest
from django.contrib.auth.models import User
from blogApp.models import Category
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile



@pytest.fixture
def admin_user(db):
    """
    Creates a superuser for admin access.
    """
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass'
    )

@pytest.fixture
def regular_user(db):
    """
    Creates a regular non-staff user.
    """
    return User.objects.create_user(
        username='regularuser',
        email='user@example.com',
        password='userpass'
    )

@pytest.fixture
def category(db):
    """
    Creates a sample category.
    """
    return Category.objects.create(name="Technology")

@pytest.fixture
def sample_image():
    """
    Creates a simple uploaded image for testing ImageField.
    """
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'\x47\x49\x46\x38\x39\x61',  # Minimal GIF header
        content_type='image/jpeg'
    )