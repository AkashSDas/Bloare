from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# User model
User = get_user_model()


# ****** Create User form in the admin page ******
class UserAdminCreationForm(forms.ModelForm):

    # Form Fields
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        max_length=20,
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        max_length=255,
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', ]

    # Validating password and confirm password and then returning confirm password
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    'Password and Confirm Password must be same')
        else:
            raise forms.ValidationError(
                'Enter both password and confirm password fields')

        return confirm_password

    # Overriding the save method
    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# ****** Update User form in the admin page ******
class UserAdminChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_staff', 'is_admin']

    def clean_password(self):
        return self.initial['password']


# ****** Signup Form for users ******
class SignupForm(forms.ModelForm):

    # Form Fields
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        max_length=20,
    )
    email = forms.EmailField(
        max_length=255,
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', ]

    # Overriding the clean method
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password and Confirm Password must be same')

        # Checking wether the username is already taken or not
        username_queryset = User.objects.filter(username=username)
        if username_queryset.exists():
            raise forms.ValidationError('This username is already taken')

        # Checking wether the email is already taken or not
        email_queryset = User.objects.filter(email=email)
        if email_queryset.exists():
            raise forms.ValidationError('This email address is already used')

        user = super(SignupForm, self).clean(*args, **kwargs)
        return user


# ****** Login Form for users ******
class LoginForm(forms.Form):

    # Form Fields
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        max_length=255,
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    )
    remember_me = forms.BooleanField(required=False)

    # Overriding the clean method
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password and Confirm Password must be same')

        if email and password:
            # Checking if the user exists or not
            user = authenticate(email=email, password=password)

            if not user:
                email_queryset = User.objects.filter(email=email)

                # Checking if user exists and has entered wrong password
                if email_queryset.exists():
                    raise forms.ValidationError('Password is incorrect')
                else:
                    raise forms.ValidationError('User does not exists')

            # Checking if the user is active or not
            if user is not None:
                if not user.is_active:
                    raise forms.ValidationError(
                        'This user is no longer active')

        user = super(LoginForm, self).clean(*args, **kwargs)
        return user
