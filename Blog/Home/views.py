import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from core.Post.models import Post
from core.Comment.models import Comment
from core.Likes.models import PostLike


def blog_index_view(request):
    return render(request, 'Blog/Home/index.html')


def blog_post_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    user = request.user
    qs = PostLike.objects.select_related('post', 'user').filter(post=post)
    likes = qs.filter(is_liked=True).count()
    dislikes = qs.filter(is_liked=False).count()

    setattr(post, 'likes', likes)
    setattr(post, 'dislikes', dislikes)

    liked, disliked = False, False
    if user.is_authenticated:
        user_qs = qs.filter(user=user)
        liked = user_qs.filter(is_liked=True).exists()
        disliked = user_qs.filter(is_liked=False).exists()
    setattr(post, 'liked', liked)
    setattr(post, 'disliked', disliked)
    return render(request, 'Blog/Home/blog_view_post.html', {'post': post})


def render_post_comment(request):
    comment_id = request.GET.get('comment_id')
    comment = get_object_or_404(Comment, pk=comment_id)
    content = render_to_string(
        'Blog/Home/blog_comment_card.html',
        {'comment': comment})
    return JsonResponse({'content': content})


def render_post_comments(request):
    data = json.loads(request.GET.get('comments'))
    content = render_to_string(
        'Blog/Home/blog_post_comments_render.html',
        {'comments': data})
    return JsonResponse({'content': content})


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
