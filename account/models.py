# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    # 将两者进行一对一的关联，用于扩展User模型。
    # 这里并没有直接使用User，而是通过一个名为AUTH_USER_MODEL来引用。
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

# Create your models here.
