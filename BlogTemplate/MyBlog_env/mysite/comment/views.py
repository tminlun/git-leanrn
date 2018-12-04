from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm
from blog.models import Blog
# Create your views here.

def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    data = {}
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, user=request.user)
        if comment_form.is_valid():#如果表单规范
            text = request.POST.get('text', '')
            comment = Comment()
            comment.user = comment_form.cleaned_data['user']
            comment.context = text
            comment.content_object = comment_form.cleaned_data['content_object']
            comment.save()
            #如果提交成功
            data['status'] = 'SUCCESS'
            #把评论数据库传给ajax / data，再把data通过ajax传递给评论列表
            data['username'] = comment.user.username
            data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%m:%S')
            data['text'] = comment.context
        else: #提交有异常
            data['status'] = 'ERROR'
            data['message'] = list(comment_form.errors.values())[0]
        return JsonResponse(data) #返回给ajax

            # return render(request,'error.html',{
            #     # 'comment_form': comment_form,
            #     # 'errors': '不能为空',
            #     'mag': comment_form.errors,
            #     'redirect_to': referer
            # })

    # if request.method == 'POST':
    #     referer = request.META.get('HTTP_REFERER', reverse('home'))#当前页得url
    #     #数据检查
    #     if not request.user.is_authenticated:#如果没有用户
    #         return render(request,'error.html', {
    #             'mag':'你尚未登录',
    #             'redirect_to':referer,#返回刚刚点击的那一页
    #         })
    #     # strip()：用户输入空格，会自动去掉。因为下面判断是否为空，空报错
    #     text = request.POST.get('text', '').strip()
    #     if text == '':
    #         return render(request,'blog/blog_detail.html',{
    #             'mag':'内容不能为空',
    #         })
    #     #如果没有这些类型
    #     try:
    #         content_type = request.POST.get('content_type', '')#获取value的值
    #         object_id = int(request.POST.get('object_id', ''))
    #         # 获取post到的类型 的具体class的模型
    #         model_class = ContentType.objects.get(model=content_type).model_class()
    #         content_object = model_class.objects.get(pk=object_id)
    #     except Exception:
    #         return render(request,'error.html',{
    #             'mag':'评论对象不存在',
    #             'redirect_to': referer,
    #         })
    #     #检查通过，实例化数据
    #     comment = Comment() #实例化评论记录
    #     comment.user = request.user
    #     comment.context = text
    #     comment.content_object = content_object #具体的对象
    #     comment.save() #保存一下
    #     return redirect(referer)

