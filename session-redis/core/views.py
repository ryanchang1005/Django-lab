from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.contrib import auth
from django.http import HttpResponseRedirect


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', context={})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if not user:
            return HttpResponseRedirect(reverse('login'))

        # 登入
        auth.login(request, user)

        return HttpResponseRedirect(reverse('dashboard'))


@login_required
def dashboard(request):
    counter = request.session.get('counter', default=0)
    counter += 1
    request.session['counter'] = counter

    return render(request, 'dashboard.html', context={
        'username': request.user.username,
        'counter': request.session['counter'],
    })
