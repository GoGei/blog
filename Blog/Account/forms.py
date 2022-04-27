from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from core.Post.models import Post


class PostForm(forms.ModelForm):
    # author = models.ForeignKey('User.User', on_delete=models.PROTECT)
    # category = models.ForeignKey('Category.Category', on_delete=models.PROTECT)
    # title = models.CharField(max_length=100, unique=True)
    # text = models.TextField()

    title = forms.CharField(label='Title', max_length=100, required=True)
    text = forms.CharField(label='Text', required=True, max_length=4048,
                           widget=CKEditorUploadingWidget(config_name='blog-post'))

    class Meta:
        model = Post
        # fields = ['title', 'text', 'category']
        fields = ['title', 'text']

    def clean_title(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        if title:
            if not Post.is_allowed_to_assign_slug(title, self.instance):
                self.add_error('title', 'This title cause ')
        return title
