from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from core.Category.models import Category


class PostForm(forms.Form):
    category = forms.ModelChoiceField(label='Category', empty_label='Select a category',
                                      queryset=Category.objects.active().all())
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', max_length=4048,
                           widget=forms.Textarea())
                           # widget=CKEditorUploadingWidget(config_name='profile'))

    class Meta:
        fields = ['title', 'text', 'category']
