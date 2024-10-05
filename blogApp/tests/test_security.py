import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from blogApp.models import Post
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile



@pytest.mark.django_db
def test_xss_protection_in_post_body(client):
    def test_xss_protection_in_post_body(client):
        # Create a post with malicious script
        post = Post.objects.create(
            title='XSS Test Post',
            body='<script>alert("XSS")</script>',
            # ...
        )

        # Get post detail page
        response = client.get(reverse('details', args=[(post.pk)]))

        # Verify script is escaped
        assert '&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;' in response.content.decode()

        # Verify HTML content
        assert '<html lang="en">' in response.content.decode()
        assert '<head>' in response.content.decode()
        assert '<body>' in response.content.decode()

        # Verify no script tags
        assert '<script>' not in response.content.decode()
