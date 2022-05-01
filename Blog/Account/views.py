import json
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django_hosts import reverse

from .forms import PostForm


def account_profile(request):
    return render(request, 'Blog/Account/profile.html')


def render_post_form(request):
    form_body = PostForm(request.GET or None)
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
