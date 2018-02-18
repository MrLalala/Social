# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Image(models.Model):
    # 制定一个一对多的外键关联。关联名为image_created
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='image_created')
    title = models.CharField(max_length=200)
    # 自动生成的字段
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='image/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    # 对于many to many的关系，django会自动创建一张表，这张表的主键使用
    # 双方主键创建。还有，关于related_name，这是双方都可以使用的
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='image_like',
                                       blank=True)

    def __str__(self):
        return self.title.decode('utf-8')

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        # 如果没添加slug字段，则自动调用title生成
        if not self.slug:
            self.slug = slugify(self.title)
            super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('images:detail', args=(self.id, self.slug))
# Create your models here.
