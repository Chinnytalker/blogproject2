from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="Home"),
    path("post/<int:pk>/", views.blog_detail, name="details"),
    path("category/<str:category_name>/", views.blog_category, name="category"),
    path("search/", views.post_search, name="search"),
    path("About/", views.about_us, name="About us"),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms_of_service, name="terms of service"),
    path('contact_us/', views.contact_us, name="Contact us"),

]
