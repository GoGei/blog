from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django_hosts import reverse
from django_hosts.resolvers import reverse as reverse_host

from .forms import LoginForm, RegistrationForm
from core.Utils.logger import log


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
            form.add_error(None, 'Please, enter correct email and password')

    return render(request, 'Blog/Login/login.html', {'form': form})


@csrf_exempt
def register_user(request):
    form = RegistrationForm(request.POST or None)

    if request.POST and request.is_ajax():
        if form.is_valid():
            user = form.save()
            log.info('User %s registered!' % user.email)
            login(request, user=user)
            rc = {
                'redirect_url': reverse('blog-index'),
                'success': True,
            }
        else:
            rc = {
                'errors': form.errors,
                'success': False,
            }
        return JsonResponse(rc)

    content = render_to_string('Blog/Login/register_form.html',
                               {'form': form,
                                'action': reverse('blog-register')},
                               request=request)
    return JsonResponse({'form': content})


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('blog-index'))
