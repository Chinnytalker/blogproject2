import pytest
from django.urls import reverse, resolve
from blogApp.views import (
    blog_index,
    blog_category,
    blog_detail,
    post_search,
    about_us,
    privacy,
    terms_of_service
)

@pytest.mark.django_db
def test_blog_index_url():
    url = reverse('Home')
    assert resolve(url).func == blog_index

@pytest.mark.django_db
def test_blog_category_url():
    category_id = 1
    url = reverse('category', args=[category_id])
    assert resolve(url).func == blog_category

@pytest.mark.django_db
def test_blog_detail_url():
    post_id = 1
    url = reverse('details', args=[post_id])
    assert resolve(url).func == blog_detail

@pytest.mark.django_db
def test_post_search_url():
    url = reverse('search')
    assert resolve(url).func == post_search

@pytest.mark.django_db
def test_about_us_url():
    url = reverse('About us')
    assert resolve(url).func == about_us

@pytest.mark.django_db
def test_privacy_url():
    url = reverse('privacy')
    assert resolve(url).func == privacy

@pytest.mark.django_db
def test_terms_of_service_url():
    url = reverse('terms of service')
    assert resolve(url).func == terms_of_service