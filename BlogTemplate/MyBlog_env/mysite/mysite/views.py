import datetime
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from read_startistics.utils import read_seven_day, popular_reading
from blog.models import Blog
from .forms import LoginForm,RegisterForm

def get_week_read():
    today = timezone.now().date()
    week = today - datetime.timedelta(days=7)#前七天
    week_read = Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=week)\
                                    .values('title','id').annotate(week_read_sum=Sum('read_details__read_num'))\
                                    .order_by('-week_read_sum')
    return week_read

def home(request):
    content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = read_seven_day(content_type)
    today_read,yesterday_read = popular_reading(content_type)

    #7天前的数据是固定的，把它放进缓存
    get_week_read = cache.get('get_week_read')
    if get_week_read is None:
        get_week_read = get_week_read
        cache.set('get_week_read', get_week_read, 3600)
        print('cache')
    else:
        print('user cache')

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_read'] = today_read
    context['yesterday_read'] = yesterday_read
    context['get_week_read'] = get_week_read
    return render(request,'home.html',context)

def Login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)#生成post的表单
        if login_form.is_valid(): #如果表单是规范的
            user = login_form.cleaned_data['user']
            login(request, user) #给他登录
            # 定向到上一级页面参数（网址）, 否则reverse返回一个网址: 参数是url.py的path的name
            return redirect(request.GET.get('from', reverse('home')))
        raise login_form.add_error(True, '输入不规范')#form表单的错误
    else: #GET
        login_form = LoginForm()
    return render(request, 'login.html',{
        'login_form': login_form,
    })

#注册
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        #如果表单通过
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)#实例化一个user
            user.save()#保存用户
            #注册完直接登录用户
            user = authenticate(username=username, password=password) #验证密码账号是否正确
            login(request, user)
            return redirect(request.GET.get('from', reverse('home'))) #重定向以前的页面

    else:
        register_form = RegisterForm()
    return render(request, 'register.html', {
        'register_form': register_form,
    })

