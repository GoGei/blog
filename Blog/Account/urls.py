from django.conf.urls import url
from Blog.Account import views


urlpatterns = [
    url('profile/$', views.account_profile, name='blog-profile'),
]
