from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from comments.models import Comment

# User model
User = get_user_model()


# ****** User's Post Model ******
class Post(models.Model):

    title = models.CharField(max_length=120, blank=False)
    content = models.TextField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(
        User, related_name='dislikes', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    # Total likes on a post
    def total_likes(self):
        return self.likes.count()

    # Total dislikes on a post
    def total_dislikes(self):
        return self.dislikes.count()

    # Returning all comments related to a specific post.
    @property
    def comments(self):
        instance = self
        query_set = Comment.objects.filter_by_instance(instance)
        return query_set

    # Returning the content type for the particular model itself and
    # thats so we can reference it wherever we need.
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
