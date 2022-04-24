from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url

from .routers import router_v1

app_name = 'api'

urlpatterns = [
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/', include((router_v1.urls, 'api'), namespace='api-v1')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
