from django.conf.urls import url
from Blog.Home import views

urlpatterns = [
    url(r'^$', views.home_index_view, name='home-index'),
]
