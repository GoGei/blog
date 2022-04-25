from django.shortcuts import render


def account_profile(request):
    return render(request, 'Blog/Account/profile.html')
