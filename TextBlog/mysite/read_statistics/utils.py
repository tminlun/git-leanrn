import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadNumDate
from myblog.models import Blog

#create your readnum

#�Ķ�����
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_reader'%(ct.model,obj.pk)
    if not request.COOKIES.get(key):
        #ÿһƪ���Ķ����� ������Ķ�����
        readnum, created = ReadNum.objects.get_or_create(content_type = ct, object_id = obj.pk)
        readnum.read_num += 1
        readnum.save()
        #�����Ķ�
        date = timezone.now().date()
        readnum, created = ReadNumDate.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readnum.read_num += 1
        readnum.save()
    return key

#ǰ������Ķ�����
def read_seven_days(content_type): #�������ĸ����͵���������Ϊ����ͨ�õĲ���ֻ���ͼ���

    today = timezone.now().date()#����
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)#�����ȥi�죬��ȥ7���������ǰ
        dates.append(date.strftime('%m/%d')) #��������
        # �������з��������Ĳ���,��������һ��app��ʱ�䣬��ΪֻҪ����ʱ�������
        readDate = ReadNumDate.objects.filter(content_type=content_type, date=date)
        result = readDate.aggregate(read_date_num=Sum('read_num'))#�����read_num���ܺ�
        read_nums.append(result['read_date_num'] or 0)#result�����Է����б��У���Ϊ���û�з���0
    return read_nums,dates #���ص����Ķ�����

#�ܵ��Ķ�����
def hot_read():
    today = timezone.now().date()
    week = today - datetime.timedelta(days=7)
    week_read = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=week) \
        .values('title', 'id').annotate(week_read_sum=Sum('read_details__read_num')) \
        .order_by('-week_read_sum')

    return week_read[:9]