from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    #class': 'form-control：设置class，把输入框拉长；placeholder：默认提示该输入什么
    username = forms.CharField(label="用户名",required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control', 'placeholder': '请输入账号',
                               }))#必须输入
    password = forms.CharField(label='密码',required=True,
                               widget=forms.PasswordInput(attrs={
                                     'class': 'form-control','placeholder': '请输入密码',
    }))

    #处理是否有问题的数据
    def clean(self):
        # post用户输入的值
        username = self.cleaned_data['username']#cleaned_data 获取用户输入的值
        password = self.cleaned_data['password']
        user = authenticate(username=username,password=password)#是否真实
        if user is not None: #账号真实
            # 如果真实把验证的user通过字典写进cleaned_date返回给views
            self.cleaned_data['user'] = user
        else: #不真实
            raise forms.ValidationError('用户账号密码输入错误')  # raise强行产生错误报告
        return self.cleaned_data #固定的,把检查完的user返回给views

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control', 'placeholder': '请输入账号',
                               }))

    email = forms.EmailField(required=True,label='邮箱',widget=forms.EmailInput(attrs={
        'class':'form-control','placeholder':'请输入邮箱',
    }))
    password = forms.CharField(required=True,min_length=6,label='密码'
                               ,widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder':'设置密码',
    }))
    password_again = forms.CharField(required=True,min_length=6,label='确认密码'
                                     ,widget=forms.PasswordInput(attrs={
            'class': 'form-control','placeholder':'请确认密码',
        }))

    #判断
    def clean_username(self):
        username = self.cleaned_data['username']
        #判断是否有重复的用户名
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
            raise forms.ValidationError('两次输入不一致')
        return password_again
