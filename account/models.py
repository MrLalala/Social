# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    # 将两者进行一对一的关联，用于扩展User模型。
    # 这里并没有直接使用User，而是通过一个名为AUTH_USER_MODEL来引用。
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    # 通过ImageField里的upload_to指定了上传的文件的保存路径。
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('following', models.ManyToManyField(
    'self', through=Contact, related_name='followers', symmetrical=False
))
# Create your models here.
