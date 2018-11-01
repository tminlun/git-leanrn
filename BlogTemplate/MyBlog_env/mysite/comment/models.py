from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.

#contenttype可以访问所有的app的model，所以可以把它作为公共的模型
class Comment(models.Model):
    #评论对象
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 评论内容
    context = models.TextField
    # 评论时间
    comment_time = models.DateTimeField(auto_now_add=True)#不能删除
    #评论的人
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) #删除评论时不删除作者

