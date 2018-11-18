from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.

#contenttype可以访问所有的app的model，所以可以把它作为公共的模型
class Comment(models.Model):
    #评论对象
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING,verbose_name="类型")
    object_id = models.PositiveIntegerField(verbose_name="类型具体ID")
    content_object = GenericForeignKey('content_type', 'object_id')
    # 评论内容、时间、作者
    context = models.TextField(verbose_name="内容",null=True,blank=True)
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name="评论的时间")#不能删除
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name="评论的作者") #删除评论时不删除作者

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ('-comment_time',)