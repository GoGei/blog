from django.conf.urls import url
from Blog.Login import views

urlpatterns = [
    url(r'login/$', views.login_view, name='blog-login'),
    url(r'logout/$', views.logout_view, name='blog-logout'),
    url(r'register/$', views.register_user, name='blog-register'),
]
