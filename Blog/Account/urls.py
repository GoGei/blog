from django.conf.urls import url
from Blog.Account import views


urlpatterns = [
    url('profile/$', views.account_profile, name='blog-profile'),
    url('render-post-form/$', views.render_post_form, name='blog-profile-post-form'),
    url('render-posts/$', views.render_posts, name='blog-profile-posts'),
]
