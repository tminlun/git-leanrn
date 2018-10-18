from django.db import models
from django.contrib.auth.models import User

class BlogType(models.Model):
    type_name = models.CharField(max_length=15,verbose_name='类型')

    def __str__(self):#不加只能显示出对象,不能显示类型名
        return self.type_name
    # def blog_count(self):
    #     return self.blog_set.all().count()

class Blog(models.Model):
    title = models.CharField(max_length=20,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING,verbose_name='博客类型')#删除博客不删除作者
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')#修改时不可以改变
    last_updated_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    def __str__(self):
        return "<Blog:%s>" % self.title
    #倒序博客
    class Meta:
        ordering = ['-created_time',]
