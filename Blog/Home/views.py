from django.shortcuts import render


def blog_index_view(request):
    return render(request, 'Blog/Home/index.html')
