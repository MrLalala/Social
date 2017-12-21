# coding:utf-8
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    # widget指定了对应的HTML输入窗体，label指定了其标签
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='Repeat Password')

    # Meta指定了使用的模型以及as_p产生的表单
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    # clean_XXXX会在is_valid时执行，如果有问题就会不通过，
    # 同理，可以将XXX换成你任意想检验的字段，
    # 如果不想让其通过，那么就raise forms.ValidationError即可。
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don`t match')
        return cd['password']
