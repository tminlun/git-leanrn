from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings #全局每一页的博客数量
from django.db.models.aggregates import Count
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from .models import Blog1,BlogType
from comment.models import Comment

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

    #获取到时间归档的数量
    blog_dates = Blog1.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates: #拿出全部时间
        date_count = Blog1.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()#筛选出博客对应的时间
        blog_dates_dict[blog_date] = date_count

    context = {}
    # Count('blog1')获取到外键的blog_type的数量
    context['blog_types'] = BlogType.objects.annotate(type_count=Count('blog1')).filter(type_name__gt=0)
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list  # 获取所有的博客
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict

    return context

def blog_list(request):
    # 留下log_all_list
    blog_all_list = Blog1.objects.all()
    # 返回字典(blog_types,page_of_blogs, ... ,blog_dates)给模板
    context = get_blog_list_common_data(request, blog_all_list)
    return render(request,'blog/blog_list.html', context)

def blogs_with_type(request, type_pk):
    blog_type = get_object_or_404(BlogType, pk=type_pk)#获取到models/BlogType/type_name
    blog_all_list = Blog1.objects.filter(blog_type=blog_type)#把models/type_name筛选给models/Blog/blog_type
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_type'] = blog_type  # 把获取到的类型 对象 传入字典
    return render(request,'blog/blogs_with_type.html',context)

def blog_dates(request,year,month):
    blog_all_list = Blog1.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_current_date'] = '%s年%s月' % (year,month)
    return render(request,'blog/blog_dates.html', context)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog1, pk = blog_pk) #当前博客
    read_cookie_key = read_statistics_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk)

    context = {}
    context['blog'] = blog
    #上一篇博客和下一篇博客
    context['previous_blog'] = Blog1.objects.filter(created_time__gt=blog.created_time).last()#前一篇博客
    context['next_blog'] = Blog1.objects.filter(created_time__lt=blog.created_time).first()
    context['user'] = request.user
    context['comments'] = comments
    response = render(request,'blog/blog_detail.html',context)#博客细节发送请求
    # 得到cookie信息（django中为字典）。浏览器把cookie信息传给服务器，true：下次访问标记已经访问过
    response.set_cookie(read_cookie_key, 'true')
    return response#返回给客户端。请求cookie的时候会把有效的cookie提交给服务器，请求包含cookie信息
