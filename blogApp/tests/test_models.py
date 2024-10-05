import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from blogApp.models import Category, Post, Comment
from django.core.files.uploadedfile import SimpleUploadedFile
import re



@pytest.mark.django_db
def test_category_model():
    # Create and test Category model
    category = Category.objects.create(name="Technology")

    assert category.name == "Technology"
    assert str(category) == "Technology"  # Assuming _str_ method returns name


@pytest.mark.django_db
def test_post_model():
    # Create a category instance
    category = Category.objects.create(name="Technology")

    # Create a user instance for 'updated_by'
    user = User.objects.create_user(username='testuser', password='testpass')

    #simulating an image upload
    image = SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg')

    # Create a post instance
    post_data = {
        'title': "Django Blog",
        'image':image,
        'body': "This is a test blog post.",
        'views': 25,
        'updated_by': user,
        'date_created': timezone.now(),
        'last_modified': timezone.now()
    }

    post = Post.objects.create(**post_data)

    post.categories.add(category)

    # Test post creation
    assert post.title == post_data['title']
    assert post.body == post_data['body']
    assert post.views == post_data['views']
    assert post.updated_by == user

    assert post.categories.count() == 1
    assert post.categories.first() == category

    # Test get_absolute_url method if it exists
    if hasattr(post, 'get_absolute_url'):
        url = reverse('details', args=[post.pk])
        assert post.get_absolute_url() == url


@pytest.mark.django_db
def test_comment_model():
    # Create category, post, and user instances
    category = Category.objects.create(name="Technology")
    user = User.objects.create_user(username='testuser', password='testpass')

    image = SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg')

    post = Post.objects.create(
        title="Django Blog",
        image=image,
        body="This is a test blog post.",
        date_created=timezone.now(),
        last_modified=timezone.now(),
        views=25,
        updated_by=user
    )
    post.categories.add(category)

    # Create a comment instance
    comment = Comment.objects.create(
        author=user,
        comment="Great blog post!",
        comment_made_on=timezone.now(),
        post=post
    )

    # Test comment creation
    assert comment.author == user
    assert comment.comment == "Great blog post!"
    assert comment.post == post
