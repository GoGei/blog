# from django.conf.urls import url, include
from rest_framework import routers

from Api.v1.Post.views import PostViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts'),
urlpatterns = router_v1.urls

urlpatterns += [
]
