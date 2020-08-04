from django.urls import path

from .views import (PostCreateView, PostDeleteView, PostDetailView,
                    PostListView, PostUpdateView, UserPostListView,
                    disliked_post_view, display_author_profile_view,
                    liked_post_view)

# ****** Url Patterns ******
urlpatterns = [
    # TODO: Change name from 'home' to 'post'
    path('home/', PostListView.as_view(), name='home'),

    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path(
        'post/<str:username>/<int:pk>/',
        display_author_profile_view,
        name='display_author_profile',
    ),
    path(
        'all-posts/<str:username>/',
        UserPostListView.as_view(),
        name='user_posts',
    ),

    path('liked/', liked_post_view, name='liked_post'),
    path('disliked/', disliked_post_view, name='disliked_post'),
]
