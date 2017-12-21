# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required


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


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {"section": 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 创建但并不保存
            # 因为在UserRegistrationForm的Meta中指定了
            # model是User，所以就是生成一个User的对象。
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # 保存用户
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})