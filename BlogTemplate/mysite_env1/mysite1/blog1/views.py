from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from .models import Blog1,BlogType

def blog_list(request):
    blog_all_list = Blog1.objects.all()
    paginator = Paginator(blog_all_list,2)#每一页10篇博客
    page_num = request.GET.get('page',10)#GET获取page页码
    page_of_blogs = paginator.get_page(page_num)#当前页面的博客内容
    current_page_num = page_of_blogs.number #获取当前页码
    page_ranges = list(range(max(current_page_num - 2, 1), current_page_num,)) + \
                  list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))


    context = {}
    context['blog_types'] = BlogType.objects.all()#获取所有的博客分类
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list#获取所有的博客
    context['page_ranges'] = page_ranges
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request,blog_pk):
    context = {}
    #可能跳转到别的页面会出错所有用404
    context['blog'] = get_object_or_404(Blog1, pk = blog_pk)
    return render_to_response('blog/blog_detail.html',context)

def blogs_with_type(request, type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=type_pk)#可能获得类型名字会出错
    context['blog_type'] = blog_type #把获取到的类型 对象 传入字典
    context['blogs'] = Blog1.objects.filter(blog_type=blog_type)#filter筛选只显示出类型
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blogs_with_type.html',context)