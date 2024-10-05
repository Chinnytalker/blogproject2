import pytest
from django.urls import reverse
from blogApp.models import Category, Post
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile



@pytest.mark.django_db
def test_blog_index_template(client):
    # Setup data
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name="Tech")

    # simulating an image upload
    image = SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg')
    Post.objects.create(
        title="First Post",
        image=image,
        body="Content for the first post.",
        date_created=timezone.now(),
        last_modified=timezone.now(),
        views=10,
        updated_by=user
    ).categories.add(category)

    # Make request
    response = client.get(reverse('Home'))

    # Check template
    assert response.status_code == 200
    assert 'blog/index.html' in [t.name for t in response.templates]
    assert 'base.html' in [t.name for t in response.templates]


    # Check context
    assert 'posts' in response.context
    assert len(response.context['posts']) == 1
    assert response.context['posts'][0].title == "First Post"

@pytest.mark.django_db
def test_about_us_template(client):
    response = client.get(reverse('About us'))
    assert response.status_code == 200
    assert 'blog/about_us.html' in [t.name for t in response.templates]
    assert 'base.html' in [t.name for t in response.templates]