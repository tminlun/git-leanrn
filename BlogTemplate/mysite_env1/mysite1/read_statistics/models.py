from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey#可以关联任何模型
from django.contrib.contenttypes.models import ContentType #引入ContentType
from django.utils import timezone
from django.db.models.fields import exceptions
from django.db.models import Sum

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)#阅读计数
    # 这里可以找到别的APP的模型（models），content_type ：别的模型的名字
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField() #对应模型主键值：数字类型
    #把content_type、object_id 哪个类型的博客对应哪个ID，筛选出来，上面content_type和ID只是字段
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExtensionMethods:#阅读扩展方法：被blog/Blog继承
    def get_read_num(self): #Blog可以用这个方法，所以self可以是Blog的对象
        try:
            ct = ContentType.objects.get_for_model(self)# models对象
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)#ReadNum对象
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

#热门博客数量
class ReadNumDate(models.Model):
    read_num = models.IntegerField(default=0)#阅读计数
    date = models.DateField(default=timezone.now)
    # 这里可以找到别的APP的模型（models），content_type ：别的模型的名字
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField() #对应模型主键值：数字类型
    #把content_type、object_id 哪个类型的博客对应哪个ID，筛选出来，上面content_type和ID只是字段
    content_object = GenericForeignKey('content_type', 'object_id')