from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import exceptions
from django.utils import timezone

# Create your models here.

#每一篇总阅读数，当天的阅读数量
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

#热门阅读
class ReadNumDate(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# 阅读数传给Blog
class ReadNumExtensionMethods:
    def get_read_num(self):
        try:
            content_type = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=content_type,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0 #没有数量返回0
