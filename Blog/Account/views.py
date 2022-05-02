import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django_hosts import reverse

from core.Post.models import Post
from .forms import PostForm


def account_profile(request):
    return render(request, 'Blog/Account/profile.html')


def render_post_form(request):
    initial_post_id = request.GET.get('post', None)
    initial_post = get_object_or_404(Post, pk=initial_post_id)
    initial = model_to_dict(initial_post)
    post_form = PostForm
    if initial_post:
        form_body = post_form(initial=initial)
    else:
        form_body = post_form()
    form = {
        'title': 'Add post',
        'body': form_body,
        'action_url': reverse('api:posts-list', host='api'),
        'buttons': {'save': True, 'cancel': True}
    }
    content = render_to_string(
        'Blog/Account/profile_post_form.html',
        {'form': form})
    return JsonResponse({'form': content})


def render_posts(request):
    posts = request.GET.get('posts', {})
    data = {}
    if posts:
        data = json.loads(posts)
    content = render_to_string(
        'Blog/Account/profile_posts.html',
        {'posts': data})
    return JsonResponse({'content': content})


def blog_profile_post_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    return render(request, 'Blog/Account/profile_post_view.html', {'post': post})
