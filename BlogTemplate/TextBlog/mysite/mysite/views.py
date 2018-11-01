from django.shortcuts import render_to_response,render,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import read_seven_days, hot_read
from myblog.models import Blog


def home(request):
    content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates=read_seven_days(content_type)
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['hot_read'] = hot_read
    return render_to_response('home.html', context)

