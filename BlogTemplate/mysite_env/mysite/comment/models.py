from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.

class Comment(models.Model):
    #评论的对象:模型和id
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING,verbose_name="类型")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id') #筛选类型条件是id和标题一致
    #评论的内容、时间、作者
    context = models.TextField(verbose_name="评论内容")
    comment_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name="作者") #删除内容，不可以删除作者的账号
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name="评论时间")#不可以改

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ('-comment_time',)

