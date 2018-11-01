import datetime
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from read_startistics.utils import read_seven_day, popular_reading
from blog.models import Blog

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
    return render_to_response('home.html',context)