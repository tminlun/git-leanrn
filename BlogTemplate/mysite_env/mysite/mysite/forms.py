from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True,min_length=3, max_length=10)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    username = forms.CharField(required=True,min_length=3)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    password_again = forms.CharField(required=True, min_length=6)

    #在form表单验证用户注册是否错误
    '''
    def clean_username(self):
        username = self.cleaned_data['username']
        # 判断后台是否有次用户名
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('密码两次输入不一致')
        return password_again
        '''

