from django.urls import path

from .views import profile_view

# ****** Url Patterns ******
urlpatterns = [
    path('profile/', profile_view, name='profile'),
]
