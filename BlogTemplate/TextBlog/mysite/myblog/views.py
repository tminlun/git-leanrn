from django.shortcuts import render,render_to_response,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import BlogType,Blog,Blog_with_news
from read_statistics.utils import read_statistics_once_read

def get_public_common_date(request,blog_of_list):
    pagingator = Paginator(blog_of_list, settings.COMMON_PAGE_NUMBER)  # 7篇一页
    page_num = request.GET.get('page', 1)
    page_of_blogs = pagingator.get_page(page_num)  # 获取使用的页码
    current_page_number = page_of_blogs.number  # 当前页码
    page_range = list(range(max(current_page_number - 2, 1), current_page_number)) + \
                 list(range(current_page_number, min(current_page_number + 2, pagingator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if pagingator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != pagingator.num_pages:
        page_range.append(pagingator.num_pages)

    #日期归档
    blog_dates = Blog.objects.dates('created_time','month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        date_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = date_count

    context = {}
    context['blogs'] = page_of_blogs.object_list  # 所有博客
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(type_count=Count('blog'))
    context['blog_date_dict'] = blog_dates_dict
    return context

#学无止境
def fengmian(request):
    blog_of_list = Blog.objects.all()
    context = get_public_common_date(request, blog_of_list)
    return render_to_response('blog/fengmian.html', context)

#博客列表
def index(request):
    context = {}
    context['blog_types'] = BlogType.objects.annotate(type_count=Count('blog'))#会返回所有分类
    return render_to_response('blog/index.html', context)
#博客细节
def info(request,blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    cookie_key = read_statistics_once_read(request,blog)#阅读记录

    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog_types'] = BlogType.objects.annotate(type_count=Count('blog'))
    response =  render_to_response('blog/info.html', context)
    response.set_cookie(cookie_key, 'true')
    return response

def time(request):
    blog_of_list = Blog.objects.all()
    context = get_public_common_date(request, blog_of_list)
    return render_to_response('blog/time.html', context)

def picture(request):
    context = {}
    return render_to_response('blog/share.html', context)

def blog_type(request,type_pk):
    blog_type = get_object_or_404(BlogType, pk=type_pk)  # type_name
    blog_of_list = Blog.objects.filter(blog_type=blog_type)
    context = get_public_common_date(request,blog_of_list)
    context['blog_type'] = blog_type # type_name

    return render_to_response('blog/blog_list.html',context)

#日期归档
def blog_date(request, year,month):
    blog_of_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_public_common_date(request,blog_of_list)
    context['date'] = '%s年%s月'%(year,month)
    return render_to_response('blog/blog_date.html',context)

#404页面
# def page_not_found(request,**kwarg):
#     from django.shortcuts import render_to_response
#     response = render_to_response('blog/Page404.html', {})
#     response.status_code = 404
#     return response