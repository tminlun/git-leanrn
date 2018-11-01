import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadNumDate
from myblog.models import Blog

#create your readnum

#阅读数量
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    date = timezone.now().date()
    key = '%s_%s_reader'%(ct.model,obj.pk)
    if not request.COOKIES.get(key):
        #每一篇总阅读数和 当天的阅读数量
        readnum, created = ReadNum.objects.get_or_create(content_type = ct, object_id = obj.pk)
        readnum.read_num += 1
        readnum.save()
        #热门阅读
        date = timezone.now().date()
        readnum, created = ReadNumDate.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readnum.read_num += 1
        readnum.save()
    return key

#前七天的阅读数量
def read_seven_days(content_type): #参数是哪个类型的数量，因为这是通用的不单只博客计数
    today = timezone.now().date()#当天
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)#当天减去i天，减去7天就是七天前
        dates.append(date.strftime('%m/%d')) #返回月日
        # 返回所有符合条件的博客,条件是哪一个app和时间，因为只要当天时间的数量
        readDate = ReadNumDate.objects.filter(content_type=content_type, date=date)
        result = readDate.aggregate(read_date_num=Sum('read_num'))#当天的read_num的总和
        read_nums.append(result['read_date_num'] or 0)#result的属性放在列表中，因为如果没有返回0
    return read_nums,dates #返回当天阅读数量

#昨天的阅读数量
def hot_read():
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_read = ReadNumDate.objects.filter(date=yesterday).order_by('-read_num')

    return yesterday_read[:7]