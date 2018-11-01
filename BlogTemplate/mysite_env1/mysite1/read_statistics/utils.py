import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadNumDate
from blog1.models import Blog1

# obj参数传入views的blog
def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj) #获得app名称
    key = ('%s_%s_read'%(ct.model, obj.pk))#ct.model：模型，cookie是一个字典，用key获得value
    if not request.COOKIES.get(key):
        #博客里的阅读总数
        ct = ContentType.objects.get_for_model(obj)  # 模型
        readnum,created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        #计算当天的全部阅读数量
        date = timezone.now().date() #当天的时间
        readnum,created = ReadNumDate.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readnum.read_num += 1
        readnum.save()
    return key

#前七天的博客(趋势图)
def read_seven_days(content_type):
    today = timezone.now().date()
    read_nums=[]
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d')) #把格式换成月和日
        readDetail=ReadNumDate.objects.filter(content_type=content_type,date=date)
        result = readDetail.aggregate(read_date_num=Sum('read_num'))
        read_nums.append(result['read_date_num'] or 0)
    return read_nums,dates

#热门阅读
def Popular_reading(content_type):
    #今天的阅读数量
    today = timezone.now().date()
        #只是对获取到的对象进行正序排序,不影响后台排序
    today_read = ReadNumDate.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    #昨天的阅读数量
    yesterday = today - datetime.timedelta(days=1)
        #Blog反向查询的昨天阅读数量,read_details是Blog和ReadNum桥梁, 分组-求和-排序
    yesterday_read = Blog1.objects.filter(read_details__date=yesterday).values('title','id')\
                                        .annotate(yesterday_read_sum = Sum('read_details__read_num'))\
                                        .order_by('-yesterday_read_sum')
    #一周热门阅读
    week = today - datetime.timedelta(days=7)
    week_read = Blog1.objects.filter(read_details__date__lt=today, read_details__date__gte=week)\
                        .values('title', 'id').annotate(week_read_sum=Sum('read_details__read_num'))\
                        .order_by('-week_read_sum')

    return today_read[:7],yesterday_read[:7],week_read[:7]
