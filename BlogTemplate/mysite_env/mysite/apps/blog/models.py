from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExtensionMethods,ReadNumDate #阅读数量

#博客分类,次文章的类型
class BlogType(models.Model):
	type_name = models.CharField(max_length=15)

	def __str__(self):
		return self.type_name

#模型(博客)
class Blog(models.Model,ReadNumExtensionMethods):
	title = models.CharField(max_length=50)
	blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
	content = RichTextUploadingField()
	author = models.ForeignKey(User,on_delete=models.DO_NOTHING) #User关联到用户
	read_details = GenericRelation(ReadNumDate)#ReadNum对象 反向查询ReadNumDate 里面有多少个对应的博客
	created_time = models.DateTimeField(auto_now_add=True)
	last_updated_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<Blog :%s>" % self.title

	#倒序博客
	class Meta:
		ordering = ['-created_time']#把最新的博客放在前面

