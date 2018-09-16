from django.shortcuts import render,render_to_response,get_object_or_404
from .models import Blog,BlogType
from django.core.paginator import Paginator
# Create your views here.

#博客首页
def blog_list(request):
    #分页
    blog_all_list = Blog.objects.all()
    paginator = Paginator(blog_all_list,10)#每页10篇
    page_num = request.GET.get('page',1)#获取页码,参数设置成page
    page_of_blogs = paginator.get_page(page_num)#解析页码内容

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list#所有的博客
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html',context)

#博客细节,因为每个博客主键不一样，所有要加主键pk来对应自己的pk
def blog_detail(request,blog_pk):
    context = {}
    #每个博客主键不唯一,所以每个博客获取到对应的主键
    context['blog'] = get_object_or_404(Blog,pk = blog_pk)
    return render_to_response('blog/blog_detail.html',context)

def blog_type(request,blog_type_pk):
    context = {}
    blog_type= get_object_or_404(BlogType,pk = blog_type_pk)
    # 博客找到(筛选)自己的类型
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_type.html',context)
