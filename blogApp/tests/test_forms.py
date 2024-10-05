import pytest
from blogApp.forms import CommentForm, SearchForm


@pytest.mark.django_db
def test_comment_form_valid_data():
    # Simulate valid form data
    form = CommentForm(data={
        'author': 'Test Author',
        'body': 'This is a test comment.'
    })

    # Check if the form is valid
    assert form.is_valid() is True

    # Check cleaned data
    assert form.cleaned_data['author'] == 'Test Author'
    assert form.cleaned_data['body'] == 'This is a test comment.'


@pytest.mark.django_db
def test_comment_form_invalid_data():
    # Simulate invalid form data (missing 'body')
    form = CommentForm(data={
        'author': 'Test Author',
        'body': ''  # Empty body
    })

    # Check if the form is invalid
    assert form.is_valid() is False

    # Check that the form has errors
    assert 'body' in form.errors  # Body is required


@pytest.mark.django_db
def test_comment_form_missing_author():
    # Simulate form data with missing author
    form = CommentForm(data={
        'author': '',  # Missing author
        'body': 'This is a test comment.'
    })

    # Check if the form is invalid
    assert form.is_valid() is False

    # Check that the form has errors
    assert 'author' in form.errors  # Author is required


@pytest.mark.django_db
def test_search_form_valid_data():
    # Simulate valid form data
    form = SearchForm(data={
        'query': 'Django'
    })

    # Check if the form is valid
    assert form.is_valid() is True

    # Check cleaned data
    assert form.cleaned_data['query'] == 'Django'


@pytest.mark.django_db
def test_search_form_invalid_data():
    # Simulate invalid form data (empty query)
    form = SearchForm(data={
        'query': ''  # Empty query
    })

    # Check if the form is invalid
    assert form.is_valid() is False

    # Check that the form has errors
    assert 'query' in form.errors  # Query is required