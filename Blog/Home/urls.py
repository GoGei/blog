from django.conf.urls import url
from Blog.Home import views

urlpatterns = [
    url(r'$', views.blog_index_view, name='blog-index'),
    url(r'render-posts/$', views.render_posts, name='blog-render-posts'),
    url(r'render-categories/$', views.render_categories, name='blog-render-categories'),
    url(r'render-post-comment/$', views.render_post_comment, name='blog-render-post-comment'),
    url(r'render-post-comments/$', views.render_post_comments, name='blog-render-post-comments'),
    url(r'post/(?P<post_slug>[\w\W\-]+)/$', views.blog_post_view, name='blog-post-view'),
]
