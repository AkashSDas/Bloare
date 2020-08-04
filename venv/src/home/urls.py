from django.urls import path

from .views import home_view

# ****** Url Patterns ******
urlpatterns = [
    path('', home_view, name='landing'), # landing page
]
