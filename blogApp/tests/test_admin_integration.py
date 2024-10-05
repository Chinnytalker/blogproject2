import pytest
from django.urls import reverse
from blogApp.models import Post
from django.utils import timezone

@pytest.mark.django_db
def test_create_post_via_admin(client, admin_user, category, sample_image):
    @pytest.mark.django_db
    def test_create_post_via_admin(client, admin_user, category, sample_image):
        # Force login as admin user
        client.force_login(admin_user)

        # Define the URL for adding a new post in the admin
        add_post_url = reverse('admin:blogApp_Post_add')

        # Ensure that the add page is accessible
        response = client.get(add_post_url)
        assert response.status_code == 200
        assert 'Add Post' in response.content.decode()

        # Prepare the data for the new post
        post_data = {
            'title': 'Integration Test Post',
            'image': sample_image,
            'body': 'This is a test post created via admin.',
            'date_created_0': timezone.now().strftime('%Y-%m-%d'),
            'date_created_1': timezone.now().strftime('%H:%M:%S'),
            'last_modified_0': timezone.now().strftime('%Y-%m-%d'),
            'last_modified_1': timezone.now().strftime('%H:%M:%S'),
            'views': 0,
            'updated_by':0,
            'categories': [(category)],
            '_save': 'Save',
        }

        # Submit the form to create a new post
        response = client.post(add_post_url, post_data, follow=True)

        # Verify that the post was created and redirected appropriately
        assert response.status_code == 200
        assert 'was added successfully' in response.content.decode()

        # Check that the post exists in the database
        assert Post.objects.filter(title='Integration Test Post').exists()
        post = Post.objects.get(title='Integration Test Post')

        # Test post attributes
        assert post.body == 'This is a test post created via admin.'
        assert post.categories.first() == category
        assert post.updated_by == admin_user
        assert post.image.name == 'test_image.jpg'

        # Test dates
        now = timezone.now()
        assert (now - post.date_created).total_seconds() < 60
        assert (now - post.last_modified).total_seconds() < 60

