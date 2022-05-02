from django.conf.urls import url
from Blog.Account import views


urlpatterns = [
    url('$', views.account_profile, name='blog-profile'),
    url('posts/$', views.render_posts, name='blog-profile-posts'),
    url('post-form/$', views.render_post_form, name='blog-profile-post-form'),
    url('post/(?P<post_slug>[\w\W\-]+)/$', views.blog_profile_post_view, name='blog-profile-post-view'),
]
