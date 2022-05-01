from django.conf.urls import url, include
from rest_framework import routers

from Api.v1.Post.views import PostViewSet
from Api.v1.Category.views import CategoryViewSet
from Api.v1.User.views import UserViewSet
from Api.v1.Comment.views import CommentViewSet

from Api.v1.Profile.urls import urlpatterns as profile_urls

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts'),
router_v1.register('categories', CategoryViewSet, basename='categories'),
router_v1.register('users', UserViewSet, basename='users'),
router_v1.register('comments', CommentViewSet, basename='comments'),
urlpatterns = router_v1.urls

urlpatterns += [
    url(r'^profile/', include(profile_urls))
]
