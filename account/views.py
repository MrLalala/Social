# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authentication!")
                else:
                    return HttpResponse('Disable account!')
            else:
                return HttpResponse("User Not found")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, })
# Create your views here.
