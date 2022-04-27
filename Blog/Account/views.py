import json

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import PostForm


def account_profile(request):
    return render(request, 'Blog/Account/profile.html')


def render_post_form(request):
    # data = json.loads(request.GET.get('posts'))
    form = PostForm(request.GET or None)
    content = render_to_string(
        'Blog/Home/blog_posts_render.html',
        {'form': form})
    return JsonResponse({'content': content})
