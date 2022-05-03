from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', max_length=255,
                             widget=forms.TextInput({'autofocus': 'autofocus',
                                                     'placeholder': 'Email address'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput({'placeholder': 'Password'}))
    remember_me = forms.BooleanField(label='Remember me', required=False)
