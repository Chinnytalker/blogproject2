import pytest
from django.urls import reverse
from django.utils import timezone
from blogApp.models import Category, Post, Comment
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_blog_index_view(client):
    # Create some sample data
    category = Category.objects.create(name="Tech")
    user = User.objects.create_user(username='testuser', password='testpass')

    # simulating an image upload
    image = SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg')

    # Create posts
    post1 = Post.objects.create(
        title="First Post",
        image=image,
        body="Content for the first post.",
        date_created=timezone.now(),
        last_modified=timezone.now(),
        views=10,
        updated_by=user
    )
    post2 = Post.objects.create(
        title="Second Post",
        image=image,
        body="Content for the second post.",
        date_created=timezone.now(),
        last_modified=timezone.now(),
        views=100,  # This will be the trending post
        updated_by=user
    )
    post1.categories.add(category)
    post2.categories.add(category)

    # Test the blog index view
    url = reverse('Home')
    response = client.get(url)

    # Check if the response is 200 OK
    assert response.status_code == 200

    # Check if the posts are in the context
    assert 'posts' in response.context
    assert post1 in response.context['posts']
    assert post2 in response.context['posts']

    # Check if trending posts are in the context
    assert 'trending_posts' in response.context
    assert post2 in response.context['trending_posts']

    # Test pagination
    assert response.context['posts'].paginator.num_pages == 1  # Adjust if more posts


@pytest.mark.django_db
def test_blog_category_view(client):
    # Create a category and posts
    category = Category.objects.create(name="Tech")
    user = User.objects.create_user(username='testuser', password='testpass')

    # simulating an image upload
    image = SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg')

    for i in range(1000):
        post1 = Post.objects.create(
            title=f"Post {i}",
            image=image,
            body="Content for the first post.",
            date_created=timezone.now(),
            last_modified=timezone.now(),
            views=10,
            updated_by=user
        )
    post1.categories.add(category)

    # Test blog category view
    url = reverse('category', args=[category.name])
    response = client.get(url)

    # Check if the response is 200 OK
    assert response.status_code == 200

    # Check if the posts are in the context
    assert 'posts' in response.context
    assert post1 in response.context['posts']

    # Test pagination
    assert response.context['posts'].paginator.num_pages == 1  # Adjust if more posts


@pytest.mark.django_db
def test_blog_detail_view(client):
    # Create post and comment data
    category = Category.objects.create(name="Tech")
    user = User.objects.create_user(username='testuser', password='testpass')

    # simulating an image upload
    image = SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg')

    post = Post.objects.create(
        title="First Post",
        image=image,
        body="Full content of the post.",
        date_created=timezone.now(),
        last_modified=timezone.now(),
        views=10,
        updated_by=user
    )
    post.categories.add(category)
    comment = Comment.objects.create(
        author=user,
        comment="This is a comment.",
        comment_made_on=timezone.now(),
        post=post
    )

    # Test blog detail view
    url = reverse('details', args=[post.id])
    response = client.get(url)

    # Check if the response is 200 OK
    assert response.status_code == 200

    # Check if the post and comments are in the context
    assert 'post' in response.context
    assert response.context['post'] == post

    assert 'comments' in response.context
    assert comment in response.context['comments']


@pytest.mark.django_db
def test_post_search_view(client):
    # Create some posts
    user = User.objects.create_user(username='testuser', password='testpass')

    # simulating an image upload
    image = SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg')

    posts = []
    for i in range(15):
        post = Post.objects.create(
            title=f"Django Test Post {1}",
            image=image,
            body="This is a post about Django testing.",
            date_created=timezone.now(),
            last_modified=timezone.now(),
            views=10,
            updated_by=user
        )
        posts.append(post)

    # Test the post search view
    url = reverse('search') + '?query=Django'
    response = client.get(url)
    context = response.context

    # Check if the response is 200 OK
    assert response.status_code == 200

    # Check if the search results are in the context
    assert 'results' in response.context
    assert any(post in context['results'] for post in posts)

    # Test pagination
    assert context['results'].paginator.num_pages == 1 # Adjust if more posts


@pytest.mark.django_db
def test_about_us_view(client):
    # Test the about us page
    url = reverse('About us')
    response = client.get(url)

    # Check if the response is 200 OK
    assert response.status_code == 200

    # Test if correct template is used (optional)
    assert 'blog/about_us.html' in [template.name for template in response.templates]
    assert 'base.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_privacy_view(client):
    # Test the privacy page
    url = reverse('privacy')
    response = client.get(url)

    # Check if the response is 200 OK
    assert response.status_code == 200

    # Test if correct template is used (optional)
    assert 'blog/privacy.html' in [template.name for template in response.templates]
    assert 'base.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_terms_of_service_view(client):
    # Test the terms of service page
    url = reverse('terms of service')
    response = client.get(url)

    # Check if the response is 200 OK
    assert response.status_code == 200

    # Test if correct template is used (optional)
    assert 'blog/terms_of_service.html' in [template.name for template in response.templates]
    assert 'base.html' in [template.name for template in response.templates]
