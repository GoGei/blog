from django import forms
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
from core.Category.models import Category
from core.Utils.fields import PhoneField


class PostForm(forms.Form):
    category = forms.ModelChoiceField(label='Category', empty_label='Select a category',
                                      queryset=Category.objects.active().all())
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', max_length=4048,
                           widget=forms.Textarea())
    # TODO add CKeditor serialization
    # widget=CKEditorUploadingWidget(config_name='profile'))


class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50,
                                 widget=forms.TextInput({'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last name', max_length=50,
                                widget=forms.TextInput({'placeholder': 'Last name'}))
    email = forms.EmailField(label='Email address', max_length=255,
                             widget=forms.TextInput({'placeholder': 'Email address'}))
    phone = PhoneField(label='Phone', widget=forms.TextInput({'placeholder': 'Phone number',
                                                              'class': 'form-control phone-number'}))


class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput({'placeholder': 'Password'}))
    repeat_password = forms.CharField(label='Repeat password',
                                      widget=forms.PasswordInput({'placeholder': 'Repeat password'}))
