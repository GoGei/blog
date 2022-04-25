from django.conf.urls import url
from Blog.Home import views

urlpatterns = [
    url(r'^$', views.blog_index_view, name='blog-index'),
]
