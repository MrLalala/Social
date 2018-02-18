# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from .forms import ImageCreateForm
from .common.decorators import ajax_required
from actions.utils import create_action


@login_required
def image_create(request):
    """
    通过使用JavaScript创建Image
    :param request:
    :return:
    """
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, "Image added successful")
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def detail(request, id, slug):
    from django.shortcuts import get_object_or_404
    from .models import Image
    image = get_object_or_404(Image, id=id, slug=slug)
    users = image.user_like.all()
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image, 'users': users})


@ajax_required
@login_required
@require_POST
def image_like(request):
    import logging
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            from .models import Image
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Exception:
            logging.warn('this is a except')
            pass
    return JsonResponse({'status': 'no'})


@require_POST
@ajax_required
@login_required
def detail_list(request):
    image_id = request.POST.get('id')
    if image_id:
        try:
            from .models import Image
            image = Image.objects.get(id=image_id)
            users = image.user_like.all()
            return render(request, 'images/image/detail_list.html', {'users': users})
        except Exception:
            import logging
            logging.warn('this is a error')
            pass
    return render(request, 'images/image/detail_list.html', {'users': None})


@login_required
def image_list(request):
    from .models import Image
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    images = Image.objects.all()
    # 4个一页
    paginator = Paginator(images, 4)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})
# Create your views here.
