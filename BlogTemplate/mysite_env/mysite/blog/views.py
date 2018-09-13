from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from .models import Blog,BlogType


def blog_list(request):
    blog_all_list = Blog.objects.all()#全部的博客列表
    paginator = Paginator(blog_all_list,10)#每一页10篇博客
    page_num = request.GET.get('page',1)#获取页码参数,get请求
    page_of_blogs = paginator.get_page(page_num) #获取当前页码的博客内容

    context = {}
    context['page_of_blogs'] = page_of_blogs#页码信息,1,2,3...上一页下一页
    # context['blogs'] = page_of_blogs.object_list #获取所有博客
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html',context)

#博客细节
def blog_detail(request,blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk = blog_pk)
    return render_to_response('blog/blog_detail.html',context)

def blogs_with_type(request,blog_with_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk = blog_with_type_pk)
    context['blog_type'] = blog_type#分类名
    context['blogs'] = Blog.objects.filter(blog_type=blog_type) #筛选显示：类型
    context['blog_types'] = BlogType.objects.all()#所有的分类
    return render_to_response('blog/blogs_with_type.html',context)


