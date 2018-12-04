from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey #可以找到多个博客
from django.db.models.fields import exceptions
from django.utils import timezone

# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)#阅读计数
    # 这里可以找到别的APP的模型（models），content_type ：别的模型的名字
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING,verbose_name="类型")
    object_id = models.PositiveIntegerField(verbose_name="当前类型主键") #对应模型主键值：数字类型
    #把content_type、object_id 变成一个通用的外键
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExtensionMethods:#阅读扩展方法：被blog/Blog继承
    def get_read_num(self): #Blog可以用这个方法，所以self可以是Blog的对象
        try:
            ct = ContentType.objects.get_for_model(self)# models对象
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)#ReadNum对象
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

#当天的阅读数量
class ReadNumDate(models.Model):
    date = models.DateField(default=timezone.now) #默认返回当天时间
    read_num = models.IntegerField(default=0) #阅读数量，数字型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField() #整数型
    content_object = GenericForeignKey('content_type','object_id') #外键获得多个博客名和ID


