from .views import ProfileView, ProfilePostsView, ProfileLikedView, ProfileSetPassword
from django.conf.urls import url
from rest_framework import routers

profile_router = routers.DefaultRouter()
profile_router.register('posts', ProfilePostsView, basename='profile-posts')
profile_router.register('posts-liked', ProfileLikedView, basename='profile-posts-liked')

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'^set-password/$', ProfileSetPassword.as_view(), name='profile-set-password')
]

urlpatterns += profile_router.urls
