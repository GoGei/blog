from django.shortcuts import render


def home_index_view(request):
    return render(request, 'Blog/Home/index.html')
