from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class BlogType(models.Model):
    type_name = models.CharField(max_length=15,verbose_name='类型名称')

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length=20,verbose_name='标题')
    content = RichTextUploadingField(verbose_name='内容')
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING,verbose_name='类型')
    reader_num = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    def __str__(self):
        return "Blog:%s"%self.title

    class Meta:
        ordering = ['-created_time']

    def contents(self):
        if len(str(self.content)) > 65:
            return '{}...'.format(str(self.content))[0:65]
        else:
            return self.content

#新闻
class Blog_with_news(models.Model):
    title = models.CharField(max_length=20,verbose_name='标题')
    content = RichTextUploadingField(verbose_name='内容')
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING,verbose_name='类型')
    reader_num = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='修改时间')
    last_time = models.DateTimeField(auto_now=True,verbose_name='创建时间')

    def __str__(self):
        return "Blog:%s"%self.title