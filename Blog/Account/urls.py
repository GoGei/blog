from django.conf.urls import url
from Blog.Account import views


urlpatterns = [
    url('$', views.account_profile, name='profile'),
    url('posts/$', views.render_posts, name='profile-posts'),
    url('post-form/$', views.render_post_form, name='profile-post-form'),
    url('post/(?P<post_slug>[\w\W\-]+)/$', views.blog_profile_post_view, name='profile-post-view'),
]
