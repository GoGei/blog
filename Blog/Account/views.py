import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django_hosts import reverse

from core.Post.models import Post
from .forms import PostForm, ProfileForm, ResetPasswordForm


@login_required
def account_profile(request):
    return render(request, 'Blog/Account/profile.html')


@login_required
def blog_profile_post_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    return render(request, 'Blog/Account/profile_post_view.html', {'post': post})


@login_required
def render_post_add_form(request):
    form_body = PostForm()
    form = {
        'title': 'Add post',
        'body': form_body,
        'method': 'POST',
        'inline_form': True,
        'action_url': reverse('api:posts-list', host='api'),
        'buttons': {'save': True, 'cancel': True}
    }
    content = render_to_string(
        'Blog/Account/profile_post_form.html',
        {'form': form})
    return JsonResponse({'form': content})


@login_required
def render_post_edit_form(request):
    initial_post_id = request.GET.get('post')
    initial_post = get_object_or_404(Post, pk=initial_post_id)
    initial = model_to_dict(initial_post)
    form_body = PostForm(initial=initial)
    form = {
        'title': 'Edit post',
        'body': form_body,
        'method': 'PUT',
        'action_url': reverse('api:posts-detail', args=[initial_post_id], host='api'),
        'buttons': {'save': True, 'cancel': True}
    }
    content = render_to_string(
        'Blog/Account/profile_post_form.html',
        {'form': form})
    return JsonResponse({'form': content})


@login_required
def render_posts(request):
    posts = request.GET.get('posts', {})
    data = {}
    if posts:
        data = json.loads(posts)
    content = render_to_string(
        'Blog/Account/profile_posts.html',
        {'posts': data})
    return JsonResponse({'content': content})


@login_required
def render_posts_liked(request):
    posts = request.GET.get('posts', {})
    data = {}
    if posts:
        data = json.loads(posts)
    content = render_to_string(
        'Blog/Account/profile_posts_liked.html',
        {'posts': data})
    return JsonResponse({'content': content})


@login_required
def render_post_delete(request):
    post_id = request.GET.get('post')
    post = get_object_or_404(Post, pk=post_id)
    content = render_to_string(
        'Blog/Account/profile_post_delete_modal.html',
        {'post': post})
    return JsonResponse({'content': content})


@login_required
def render_post(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, pk=post_id)
    content = render_to_string(
        'Blog/Account/profile_post_card.html',
        {'post': post})
    return JsonResponse({'content': content})


@login_required
def render_profile_form(request):
    user = request.user
    initial = model_to_dict(user)
    form_body = ProfileForm(initial=initial)
    form = {
        'body': form_body,
        'method': 'PUT',
        'action_url': reverse('api:profile', host='api'),
    }

    content = render_to_string(
        'Blog/Account/profile_edit_profile_form.html',
        {'form': form})
    return JsonResponse({'content': content})


@login_required
def render_profile_password_form(request):
    form = {
        'body': ResetPasswordForm(),
        'action_url': reverse('api:profile-set-password', host='api'),
    }

    content = render_to_string(
        'Blog/Account/profile_password_profile_form.html',
        {'form': form})
    return JsonResponse({'content': content})
