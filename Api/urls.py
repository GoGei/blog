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


if settings.API_DOCUMENTATION:
    from rest_framework import permissions
    from drf_yasg2.views import get_schema_view
    from drf_yasg2 import openapi

    api_urlpatterns = [
        url(r'^v1/', include((router_v1.urls, 'Api'), namespace='api')),
    ]
    api_url = '%s://api%s' % (settings.SITE_SCHEME, settings.PARENT_HOST)

    if settings.HOST_PORT:
        api_url = '%s://api%s:%s' % (settings.SITE_SCHEME, settings.PARENT_HOST, settings.HOST_PORT)

    schema_view = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version='v1',
        ),
        url=api_url,
        patterns=api_urlpatterns,
        public=True,
        permission_classes=(permissions.AllowAny, ),
    )

    urlpatterns += [
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
