import datetime
from django.shortcuts import redirect,render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from read_statistics.utils import read_seven_days,get_today_hot_date, get_yesterday_hot_date
from blog.models import Blog
from .forms import LoginForm,RegisterForm


#方便传入,一周内的热门阅读: 大于等于前七天、小于今天
def get_week_read_nums():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)  # 前七天
    #前七天的博客 当前在Blog模型里面，要获取ReadNum模型的字段： read_details__date/read_details__read_num
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
                                .values('title', 'id')\
                                .annotate(week_read_sum=Sum('read_details__read_num'))\
                                .order_by('-week_read_sum')
    return blogs[:7]

# 总首页
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = read_seven_days(blog_content_type)
    #获取热门博客缓存数据
    week_hot_dates = cache.get('week_hot_dates')#获取 一周热门阅读的打的方法（context['week_hot_dates']）
    #如果获取的热门key为空，将写入缓存，不为None提示 user cache
    if week_hot_dates is None:
        get_week_read = get_week_read_nums()#周热门方法赋值给个变量
        cache.set('week_hot_dates', get_week_read , 3600) #写进缓存 key, value, time（单位：秒）
    else:
        print('user cache')
    context = {}  # 不需要传入其他东西
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_dates'] = get_today_hot_date(blog_content_type)
    context['yesterday_hot_dates'] = get_yesterday_hot_date(blog_content_type)
    context['week_hot_dates'] = get_week_read_nums()

    return render(request, 'home.html', context)


def login(request): #action 在这个url的views处理
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():#如果输入的值是规范的
            username = login_form.cleaned_data['username'] #获取用户输入的username
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password) #验证是否真实,不真实返回None
            if user is not None: #如果真实
                auth.login(request, user)#给他登录
                return redirect(request.GET.get('from', reverse('home')))
            else:
                login_form.add_error(None, '账号或者密码错误')
    else:#get
        login_form = LoginForm()
    return render(request, 'login.html',{
        'login_form': login_form,
    })


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            password_again = register_form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {
                    'register_form': register_form,
                    'msg': '已经有此用户',
                })
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html',{
                    'register_form': register_form,
                    'msg': '已经有此邮箱',
                })
            if password != password_again:
                return render(request, 'register.html',{
                    'msg': '两次输入不一致',
                })

            user = User.objects.create_user(username, email, password) #创建用户
            user.save()
            user = auth.authenticate(username=username, email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegisterForm()
    return render(request, 'register.html',{
        'register_form': register_form,
    })


