import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadNumDate


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)  # obj相当于blog
    key = "%s_%s_pk" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 每一篇博客阅读总数
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        # 每一天的阅读数量
        date = timezone.now().date()  # 当天时间
        readDate, created = ReadNumDate.objects.get_or_create(content_type=ct, object_id=obj.pk,
                                                              date=date)  # 返回全部当天时间阅读数量
        readDate.read_num += 1
        readDate.save()
    return key

#content_type哪个类型
def read_seven_day(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        week = today - datetime.timedelta(days=i)
        dates.append(week.strftime('%m/%d'))
        read_deta = ReadNumDate.objects.filter(content_type=content_type,date=week)
        result = read_deta.aggregate(week_sum=Sum('read_num'))
        read_nums.append(result['week_sum'] or 0)
    return read_nums,dates

#热门阅读
def popular_reading(content_type):
    #今天的博客阅读数,今天只有一个日期对象，所以不用求和
    today = timezone.now().date()
    today_read = ReadNumDate.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    #昨天的热门阅读，也是单个日期（单个对象）
    yesterday = today - datetime.timedelta(days=1)
    yesterday_read = ReadNumDate.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
    return today_read[:7],yesterday_read[:7]

