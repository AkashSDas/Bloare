from django.urls import path

from .views import CommentDeleteView, CommentUpdateView

# ****** Url Patterns ******
urlpatterns = [
    path(
        'comment/<int:pk>/update/', CommentUpdateView.as_view(), name="comment_update"
    ),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"
    ),
]
