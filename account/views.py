# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from images.common.decorators import ajax_required
from .models import Contact


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
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    from django.contrib import messages
    if request.method == 'POST':
        # 将实例指定为request的用户,指定数据来源
        # 通常对于含有两个Model的表单的处理皆是如此。。。
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        # 通过一对一的关系，使用request.user找到对应的profile
        # 对于一些特殊的Model，如含有文件的，要指定其文件来源。。？
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_list(request):
    from django.contrib.auth.models import User

    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    from django.shortcuts import get_object_or_404
    from django.contrib.auth.models import User

    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})


@require_POST
@ajax_required
@login_required
def user_follow(request):
    from django.contrib.auth.models import User
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except:
            return JsonResponse({'status': 'no'})
    return JsonResponse({'status': 'no'})
