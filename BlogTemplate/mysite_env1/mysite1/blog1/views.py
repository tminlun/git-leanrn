from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings #全局每一页的博客数量
from .models import Blog1,BlogType

def get_blog_list_common_data(request, blog_all_list):
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOG_NUMBER)  # 每一页10篇博客
    page_num = request.GET.get('page', 1)  # GET获取page页码
    page_of_blogs = paginator.get_page(page_num)  # 当前页面的博客内容
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码的前后2页页码
    page_range = list(range(max(current_page_num - 2, 1), current_page_num, )) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 添加省略号(因为下面添加第一页永远都是1，1 - 1 = 0,得不到>=2,所以得不到...)
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
        # 如果总页 - 最后一页 大于等于2
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 如果页码范围, 第一个页码不等于 1
    if page_range[0] != 1:
        page_range.insert(0, 1)  # 第一个页码插入数字为1的页码
    # 如果最后一页不等于总页数
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)  # 把总页加上
    context = {}
    context['blog_types'] = BlogType.objects.all()  # 获取所有的博客分类
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list  # 获取所有的博客
    context['page_range'] = page_range
    context['blog_dates'] = Blog1.objects.dates('created_time', 'month', order='DESC')
    return context

def blog_list(request):
    # 留下log_all_list
    blog_all_list = Blog1.objects.all()
    # 返回字典(blog_types,page_of_blogs, ... ,blog_dates)给模板
    context = get_blog_list_common_data(request, blog_all_list)
    return render_to_response('blog/blog_list.html', context)

def blogs_with_type(request, type_pk):
    blog_type = get_object_or_404(BlogType, pk=type_pk)  # 可能获得类型名字会出错
    blog_all_list = Blog1.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_type'] = blog_type  # 把获取到的类型 对象 传入字典
    return render_to_response('blog/blogs_with_type.html',context)

def blog_dates(request,year,month):
    blog_all_list = Blog1.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_current_date'] = '%s年%s月' % (year,month)
    return render_to_response('blog/blog_dates.html', context)

def blog_detail(request,blog_pk):
    context = {}
    #可能跳转到别的页面会出错所有用404
    blog = get_object_or_404(Blog1, pk = blog_pk)
    context['blog'] = blog
    #上一篇博客和下一篇博客
    context['previous_blog'] = Blog1.objects.filter(created_time__gt=blog.created_time).last()#前一篇博客
    context['next_blog'] = Blog1.objects.filter(created_time__lt=blog.created_time).first()
    return render_to_response('blog/blog_detail.html',context)
