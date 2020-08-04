from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm


# ****** Signup View ******
def signup_view(request, *args, **kwargs):
    _next = request.GET.get('next')

    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        if _next:
            return redirect(_next)
        return redirect('/accounts/login/')

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


# ****** Login View ******
def login_view(request, *agrs, **kwargs):
    _next = request.GET.get('get')

    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)

        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

        if _next:
            return redirect(_next)
        return redirect('/profiles/profile/')

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


# ****** LogOut View ******
def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html', {})
