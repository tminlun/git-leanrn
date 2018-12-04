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
    #related_name = "comments":给user.comment_set.all()定义个名字而已：（数据库Comment可以查询顶级评论作者）user也可以反向查询数据库所有顶级评论
    user = models.ForeignKey(User,related_name="comments", on_delete=models.DO_NOTHING,verbose_name="顶级评论者") #删除评论时不删除作者
    """
        回复最顶级的评论：root
        user：顶级评论者 用户
    """
    #在外面找顶级评论的id
    # parent_id = models.IntegerField(default=0, verbose_name="父级id")
    #此数据库（self）的所有评论,可以直接在"添加记录"里面(更方便)查找顶级评论。【就不用使用刚刚的方法：在外面查找顶级评论的ID】
    parent = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING, verbose_name="查询顶级评论的内容")

    """
        回复谁：reply_to
        取出回复顶级评论 的回复者 的姓名
    """
    #回复谁（不一定顶级评论有人回复他，可以为空。【related_name="reply_comment_user"：给user.comment_set.all()定义一个名字】
    reply_to = models.ForeignKey(User,null=True, related_name="replys",on_delete=models.DO_NOTHING,verbose_name="回复顶级评论的作者")
    """
        回复的评论：root
    """
    # root = models.ForeignKey('self',null=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.context

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ('-comment_time',)