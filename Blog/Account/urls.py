from django.conf.urls import url
from Blog.Account import views


urlpatterns = [
    url('$', views.account_profile, name='profile'),
    url('render-posts/$', views.render_posts, name='profile-posts'),
    url('render-post-add-form/$', views.render_post_add_form, name='profile-post-add-form'),
    url('render-post-edit-form/$', views.render_post_edit_form, name='profile-post-edit-form'),
    url('render-post-delete-form/$', views.render_post_delete, name='profile-post-delete-form'),
    url('render-post/$', views.render_post, name='profile-render-post'),
    url('render-profile-form/$', views.render_profile_form, name='profile-render-profile-form'),
    url('post/(?P<post_slug>[\w\W\-]+)/$', views.blog_profile_post_view, name='profile-post-view'),
]
