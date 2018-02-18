# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey(User, related_name='actions', db_index=True)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    # 用来连接ContentType所要模拟的Model
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj')
    # 用来表示使用ContentType表示的Model的主键值
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    # 指定管理关系
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ('-created', )

# Create your models here.
