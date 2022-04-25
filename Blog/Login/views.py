from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_hosts import reverse

from core.User.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('blog-index'))
    user = User.objects.get(email='rich.290401@gmail.com')
    login(request, user=user)
    return render(request, 'Blog/Login/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('blog-index'))
