from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from blog1.models import Blog1
from read_statistics.utils import read_seven_days,Popular_reading



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
	return render_to_response('home.html',context)

def blog_picture(request):
	context = {}
	return render_to_response('index.html',context)
