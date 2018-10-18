from django.shortcuts import render,render_to_response,get_object_or_404
from .models import BlogType,Blog,Blog_with_news
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count

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

    context = {}
    context['blogs'] = page_of_blogs.object_list  # 所有博客
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(type_count=Count('blog'))
    return context

def fengmian(request):
    blog_of_list = Blog.objects.all()
    context = get_public_common_date(request, blog_of_list)
    return render_to_response('blog/fengmian.html', context)


def index(request):
    context = {}
    context['blog_types'] = BlogType.objects.annotate(type_count=Count('blog'))#会返回所有分类
    return render_to_response('blog/index.html', context)

def info(request,blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog_types'] = BlogType.objects.annotate(type_count=Count('blog'))
    #阅读数量
    if not request.COOKIES.get('blog_%s_reader'%blog.pk):
        blog.reader_num += 1
        blog.save()
    response =  render_to_response('blog/info.html', context)
    response.set_cookie('blog_%s_reader'%blog.pk, 'true')
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
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return render_to_response('blog/blog_list.html',context)

#404页面
# def page_not_found(request,**kwarg):
#     from django.shortcuts import render_to_response
#     response = render_to_response('blog/Page404.html', {})
#     response.status_code = 404
#     return response