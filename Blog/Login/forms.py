from django import forms
from core.User.models import User
from core.Utils.fields import PhoneField


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', max_length=255,
                             widget=forms.TextInput({'autofocus': 'autofocus',
                                                     'placeholder': 'Email address'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput({'placeholder': 'Password'}))
    remember_me = forms.BooleanField(label='Remember me', required=False)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50,
                                 widget=forms.TextInput({'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last name', max_length=50,
                                widget=forms.TextInput({'placeholder': 'Last name'}))
    email = forms.EmailField(label='Email address', max_length=255,
                             widget=forms.TextInput({'placeholder': 'Email address'}))
    phone = PhoneField(label='Phone', widget=forms.TextInput({'placeholder': 'Phone number',
                                                              'class': 'form-control phone-number'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput({'placeholder': 'Password'}))
    repeat_password = forms.CharField(label='Repeat password',
                                      widget=forms.PasswordInput({'placeholder': 'Password'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_qs = User.objects.filter(email__iexact=email)
        if user_qs.exists():
            self.add_error('email', 'This email already exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user_qs = User.objects.filter(phone=phone)
        if user_qs.exists():
            self.add_error('phone', 'This phone already exists')
        return phone

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        repeated_password = cleaned_data.get('repeat_password')
        if password and repeated_password and password != repeated_password:
            self.add_error('password', 'Password mismatch!')
            self.add_error('repeat_password', 'Password mismatch!')

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        excluded_fields = ['repeat_password']
        [cleaned_data.pop(key, None) for key in excluded_fields]
        user = User.objects.create_user(**cleaned_data)
        user.save()
        return user
