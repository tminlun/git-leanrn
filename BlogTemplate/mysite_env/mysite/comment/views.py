from django.shortcuts import render,redirect,HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Comment
# Create your views here.

def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    #post到from的值
    if request.POST:
        if not request.user.is_authenticated:
            return render(request, 'errer.html', {
                'msg': '没有登录',
                'referer': referer,
            })
        text = request.POST.get('text', '').strip()
        if text == '':
            return render(request,'errer.html',{
               'msg': '内容不能为空',
                'referer':referer,
            })
        try:
            content_type = request.POST.get('content_type', '')
            object_id = request.POST.get('object_id', '')
            model_class = ContentType.objects.get(model=content_type).model_class()  # 获取模型（class）
            content_object = model_class.objects.get(pk=object_id)  # 具体的对象
        except Exception:
            return render(request, 'errer.html', {
                'msg': '获取不到对象',
                'referer': referer,
            })
        #得到值实例化评论
        comment = Comment()
        comment.comment_user = request.user
        comment.context = text
        comment.content_object = content_object
        comment.save() #保存评论
        return redirect(referer)
