from django.contrib.auth import views as auth_view
from django.urls import path

from .views import login_view, logout_view, signup_view

# ****** Url Patterns ******
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # *** Password Reset Urls ***
    path(
        'password-reset/',
        auth_view.PasswordResetView.as_view(
            template_name='accounts/password-reset.html'
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_view.PasswordResetDoneView.as_view(
            template_name='accounts/password-reset-done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_view.PasswordResetConfirmView.as_view(
            template_name='accounts/password-reset-confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_view.PasswordResetCompleteView.as_view(
            template_name='accounts/password-reset-complete.html'
        ),
        name='password_reset_complete',
    ),
]
