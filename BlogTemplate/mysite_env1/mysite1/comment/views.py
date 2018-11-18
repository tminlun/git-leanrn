from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Comment
# Create your views here.

def update_comment(request):
    if request.POST:
        referer = request.META.get('HTTP_REFERER', reverse('home'))
        if not request.user.is_authenticated:
            return render(request,'error.html',{
                'message':'未登录',
                'referer':referer,
            })

        text = request.POST.get('text', '').strip()
        if text == '':
            return render(request, 'blog/blog_detail.html',{
                'msg': '输入不能为空',
            })
        try:
            content_type = request.POST.get('content_type', '')
            object_id = request.POST.get('object_id', '')
            # get_for_model只能获取页面传递的类型（对象）,不能获取次类型的模型
            # model_class可以获得模型（class），从而获取此类型的具体的博客（content_object：具体的类型）
            model_class = ContentType.objects.get(model=content_type).model_class()
            obj = model_class.objects.get(pk=object_id)  # 获得具体的类型
        except Exception:
            return render(request,'error.html',{
                'message': '没有此对象',
                'referer': referer,
            })

        comment = Comment()#实例化评论
        comment.comment_user = request.user
        comment.context = text
        comment.content_object = obj #把具体的博客传递给content_object（具体的类型）
        comment.save()
        return redirect(referer)

