from django.shortcuts import render_to_response,get_object_or_404
from .models import Blog1,BlogType

def blog_list(request):
    context = {}
    context['blogs'] = Blog1.objects.all()#获取所有的博客
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request,blog_pk):
    context = {}
    #可能跳转到别的页面会出错所有用404
    context['blog'] = get_object_or_404(Blog1, pk = blog_pk)
    return render_to_response('blog/blog_detail.html',context)

def blogs_with_type(request, type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType,pk=type_pk)#可能获得类型名字会出错
    context['blogs'] = Blog1.objects.filter(blog_type=blog_type)#filter筛选只显示出类型
    context['blog_type'] = blog_type #把获取到的类型 对象 传入字典
    return render_to_response('blog/blogs_with_type.html',context)