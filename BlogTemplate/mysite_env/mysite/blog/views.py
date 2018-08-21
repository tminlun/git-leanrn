from django.shortcuts import render_to_response,get_object_or_404
from .models import Blog,BlogType


def blog_list(request):
    blog = Blog.objects.all()
    context = {}
    context['blogs'] = blog
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
    context['blogs'] = Blog.objects.filter(blog_type=blog_type) #筛选显示：类型
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html',context)


