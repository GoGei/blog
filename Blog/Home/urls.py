from django.conf.urls import url
from Blog.Home import views

urlpatterns = [
    url(r'$', views.blog_index_view, name='blog-index'),
    url(r'render-posts/$', views.render_posts, name='blog-render-posts'),
    url(r'render-categories/$', views.render_categories, name='blog-render-categories'),
    url(r'post/(?P<post_slug>[\w\W\-]+)/$', views.blog_post_view, name='blog-post-view'),
]
