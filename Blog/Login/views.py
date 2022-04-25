from django.shortcuts import render


def login_view(request):
    return render(request, 'Blog/Login/login.html')


def register_view(request):
    return render(request, 'Blog/Login/register.html')


def logout_view(request):
    return render(request, 'Blog/Login/logout.html')
