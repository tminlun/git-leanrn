from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog,BlogType

#获取博客列表共同的数据,设置参数blog_all_list全部博客,因为每个方法都有不同的获取方法
def get_blog_list_common_data(request, blog_all_list):
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOG_NUMBER)  # 每一页10篇博客
    page_num = request.GET.get('page', 1)  # 获取页码参数,get请求
    page_of_blogs = paginator.get_page(page_num)  # 获取当前页码
    current_page_num = page_of_blogs.number  # 获取当前页码
    # current_page_num - 2 , 1 只是拿1和currentr_page_num - 2比，range范围还是
    # current_page_num - 2, currentr_page_num
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 添加省略
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    # 如果总页 - 最后一页 大于等于2
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 添加第一页和最后一页
    if page_range[0] != 1:
        page_range.insert(0, 1)  # 将第一个页码变成1(insert在第一个插入)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)  # 添加总页码到最后显示页码(append在尾部添加)

    context = {}
    context['page_range'] = page_range  # 返回对象给模板
    context['page_of_blogs'] = page_of_blogs  # 页码信息,1,2,3...上一页下一页
    context['blogs'] = page_of_blogs.object_list  # 获取所有博客
    context['blog_types'] = BlogType.objects.all()
    # 获取到全部的年和月
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return context #返回给模板 render_to_response('？.html',context)

def blog_list(request):
    blog_all_list = Blog.objects.all()#全部的博客列表
    context = get_blog_list_common_data(request,blog_all_list) #传递给context
    return render_to_response('blog/blog_list.html',context)

def blogs_with_type(request,blog_with_type_pk):
    blog_type = get_object_or_404(BlogType,pk = blog_with_type_pk)#获取分类
    blog_all_list = Blog.objects.filter(blog_type=blog_type)#获取所有筛选类型博客
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_type'] = blog_type  # 分类名
    return render_to_response('blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    #获取到对应年和月的博客
    blog_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_with_date'] = "%s年%s月"  %(year,month) #当前的年月
    return render_to_response('blog/blogs_with_date.html',context)

#博客细节
def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk = blog_pk)
    context['blog'] = blog
    #前一篇博客，大于：__gt=
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    #后一篇博客，小于：__lt=
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    return render_to_response('blog/blog_detail.html',context)
