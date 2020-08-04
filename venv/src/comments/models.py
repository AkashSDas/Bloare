from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# User model
User = get_user_model()


# ****** Comment Manager ******
class CommentManager(models.Manager):

    # Overriding the all method
    # This will return a query_set of Comment that do not have parents.
    # To make sure this works perfectly we have to make filter_by_instance
    # also filters Comment where parent=None.
    def all(self):
        query_set = super(CommentManager, self).filter(parent=None)
        return query_set

    # This method is to make our comments filter by instance.
    # Here we used to ContentType which makes the `comment` app more independent.
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        query_set = (
            super(CommentManager, self)
            .filter(content_type=content_type, object_id=object_id)
            .filter(parent=None)
        )
        return query_set


# ****** Comment ******
class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.user.username

    # Replies to a Comment (Replies are childerns of a Comment)
    def childern(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
