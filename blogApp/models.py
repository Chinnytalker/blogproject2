from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
         verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField("category", related_name="posts")
    updated_by = models.CharField(max_length=100,)

    def increment_views(self):
        self.views += 1
        self.save()

    def get_absolute_url(self):
        return reverse('details', args=[str(self.pk)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=50)
    comment = models.TextField()
    comment_made_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return self.author










