from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation #反向查询
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNumDate,ReadNumExtensionMethods#阅读数量


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
class Blog1(models.Model,ReadNumExtensionMethods):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadNumDate) #反向查询ReadNum
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='img',null=True,blank=True)

    # def get_read_num(self): #Blog可以用这个方法，所以self可以是Blog的对象
    #     try:
    #         ct = ContentType.objects.get_for_model(self)# models对象
    #         readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)#ReadNum对象
    #         return readnum.read_num
    #     except exceptions.ObjectDoesNotExist:
    #         return 0

    #显示出最新的博客，历史博客放后面
    class Meta:
        ordering = ['-created_time']

    #后台限制内容字数
    def contents(self):
        if len(str(self.content)) > 65:
            return '{}...'.format(str(self.content))[0:65]
        else:
            return self.content

    def __str__(self):
        return "<Blog1: %s>" % self.title
