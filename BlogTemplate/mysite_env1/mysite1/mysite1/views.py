from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from blog1.models import Blog1
from read_statistics.utils import read_seven_days,Popular_reading
from .forms import LoginForm,RegisteredForm


def home(request):
	ct = ContentType.objects.get_for_model(Blog1)
	read_nums,dates = read_seven_days(ct) #趋势图
	today_read, yesterday_read, week_read = Popular_reading(ct) #昨天和今天

	#获取和写入缓存数据：1、先得到哪个方法需要缓存。2、判断方法是否写入，如果空则写入
	week_read = cache.get('week_read')  # 记得加 ''
	if week_read is None:
		week_read = week_read
		cache.set('week_read', week_read, 3600)
		print('cache')
	else:
		print('user cache')

	context = {}
	context['read_nums'] = read_nums
	context['dates'] = dates
	context['today_read'] = today_read
	context['yesterday_read']=yesterday_read
	context['week_read'] = week_read
	return render(request,'home.html',context)

def blog_picture(request):
	context = {}
	return render(request,'index.html',context)

def login(request):

	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			user = auth.authenticate(username=username, password=password) #后台是否有此账号密码
			if user is not None:
				auth.login(request, user)
				return redirect(request.GET.get('from', reverse('home')))
			else:
				return render(request, 'login.html', {
					'login_form': login_form,
					'error': '没有此用户',
				})
		else:
			return render(request, 'login.html', {
				'login_form': login_form,
				'error':'输入账号或者密码错误',
			})
	else:
		login_form = LoginForm()
	return render(request, 'login.html',{
		'login_form': login_form,
	})

def registered(request):
	if request.method == 'POST':
		registered_form = RegisteredForm(request.POST)
		if registered_form.is_valid():
			username = registered_form.cleaned_data['username']
			email = registered_form.cleaned_data['email']
			password = registered_form.cleaned_data['password']
			password_again = registered_form.cleaned_data['password_again']
			if User.objects.filter(username=username).exists():
				return render(request, 'registered.html',{
					'registered_form': registered_form,
					'errors':'已经有此用户'
				})
			if User.objects.filter(email=email).exists():
				return render(request, 'registered.html',{
					'registered_form': registered_form,
					'errors':'已经有此邮箱'
				})
			if password != password_again:
				return render(request, 'registered.html', {
					'registered_form': registered_form,
					'errors': '两次输入不匹配'
				})
			user = User.objects.create_user(username,email,password)
			user.save()
			user = auth.authenticate(username=username,email=email,password=password)#保存到后台后要登录
			if user is not None:
				auth.login(request, user)
				return redirect(request.GET.get('from', reverse('home')))
			else:
				return render(request, 'registered.html', {
					'registered_form': registered_form,
					'errors': '没有注册成功哦'
				})
		else:
			return render(request, 'registered.html', {
				'registered_form': registered_form,
				'errors': '输入错误'
			})
	else:
		registered_form = RegisteredForm()
	return render(request, 'registered.html',{
		'registered_form': registered_form,
	})
