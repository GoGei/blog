from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django_hosts import reverse
from django_hosts.resolvers import reverse as reverse_host

from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('blog-index'))

    initial = {'email': request.COOKIES.get('email', '')}
    form = LoginForm(request.POST or None,
                     initial=initial)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            if user.is_active:
                login(request, user=user)

                remember_me = data['remember_me']
                if not remember_me:
                    request.session.set_expiry(0)
                    request.session.modified = True

                response = HttpResponseRedirect(reverse_host('blog-index', host='blog'))
                response.set_cookie('email', user.email)
                return response
            else:
                form.add_error(None, 'This account is not active')
        else:
            form.add_error(None, 'Account with this credentials does not exists')

    return render(request, 'Blog/Login/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('blog-index'))
