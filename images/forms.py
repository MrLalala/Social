# coding: utf-8
from django import forms
from .models import Image
from urllib import urlopen
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            # 生成一个type = hidden的HTML标签元素，意味着用户看不见
            # 通过widgets字典指定字段的对应HTML标签
            'url': forms.HiddenInput,
        }

    # 在 is_valid()方法调用时执行
    def clean_url(self):
        # 获取表单图片的url
        url = self.cleaned_data['url']
        # 指定合法的图片类型
        valid_extension = ['jpg', 'jpeg']
        # 将url进行分离。分隔符为'.'，最多分离一次。
        # 得到由两个元素的组成的元组，第一个为文件名，第二个是文件类型。
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extension:
            raise forms.ValidationError("The given URL doesn't valid")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        # 通过指定commit参数为False，生成一个临时的image对象
        image = super(ImageCreateForm, self).save(commit=False)
        # 获取url值
        image_url = self.cleaned_data['url']
        # 生成图片名称
        image_name = "{}.{}".format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
        # 打开这个图片的url并保存在本地
        response = urlopen(image_url)
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        # 保证在commit参数为True时在保存对象。配合view查看效果更佳。
        if commit:
            image.save()
        # 返回该图片对象。
        return image