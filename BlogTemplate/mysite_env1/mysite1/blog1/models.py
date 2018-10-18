from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

#博客分类模型
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return self.type_name
    """
    #统计数量方法2：反过来用 type_name的id(如：1)来查询 blog_type对应的id(如：1)
    def blog_type_count(self):
        return self.blog1_set.all().count()
    """
class Blog1(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog1: %s>" % self.title

    #显示出最新的博客，历史博客放后面
    class Meta:
        ordering = ['-created_time']

    #阅读数量
    '''def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist: #不存在
            return 0
            '''

    def contents(self):
        if len(str(self.content)) > 65:
            return '{}...'.format(str(self.content))[0:65]
        else:
            return self.content

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog1, on_delete=models.DO_NOTHING)#传入外键，一对一
    '''




