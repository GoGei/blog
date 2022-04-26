import json

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string


def blog_index_view(request):
    return render(request, 'Blog/Home/index.html')


def render_posts(request):
    data = json.loads(request.GET.get('posts'))
    content = render_to_string(
        'Blog/Home/blog_posts_render.html',
        {'posts': data})
    return JsonResponse({'content': content})


def render_categories(request):
    data = json.loads(request.GET.get('categories'))

    content = render_to_string(
        'Blog/Home/blog_categories_render.html',
        {'categories': data},
        request=request)
    return JsonResponse({'content': content})
