import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum,ReadNumDate
from django.db.models import Sum

def read_statistics_once_read(request, obj):#继承blog_detail(request,blog_pk)的request
    ct = ContentType.objects.get_for_model(obj) #obj相当于blog
    key = "%s_%s_pk"%(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        #每一篇博客阅读总数
        readnum,created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        #每一天的阅读数量
        date = timezone.now().date()#当天时间
        readDate,created = ReadNumDate.objects.get_or_create(content_type=ct, object_id=obj.pk,date=date)#返回全部当天时间阅读数量
        readDate.read_num += 1
        readDate.save()
    return key #返回给detail的set_cookie(key, 'true')

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

#今天热门阅读
def get_today_hot_date(content_type):
    today = timezone.now().date()
    read_details = ReadNumDate.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7] #取前七条
#昨天
def get_yesterday_hot_date(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadNumDate.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')#昨天的博客对象
    return read_details[:7] #取前七条



