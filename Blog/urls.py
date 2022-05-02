from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('urls')),
    url(r'', include('Blog.Login.urls')),
    url(r'^', include('Blog.Home.urls')),
    url(r'^account/', include('Blog.Account.urls')),
]
