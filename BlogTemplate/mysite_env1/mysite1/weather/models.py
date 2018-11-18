from django.db import models
# Create your models here.

class Weather(models.Model):
    currentCity = models.CharField(max_length=10,verbose_name="城市名")  # 城市名
    pm25 = models.CharField(max_length=10, verbose_name="PM25")
    data = models.CharField(max_length=10,verbose_name="日期")  # 日期
    Picture = models.ImageField(verbose_name="图片")  # 天气图片
    the_weather = models.CharField(max_length=10,verbose_name="气候") #天气
    temperature = models.CharField(max_length=15,verbose_name="温度",null=True, blank=True)
    today_or_future = models.IntegerField(default=1,verbose_name="天气日期类型")

    class Meta:
        verbose_name = "天气"
        verbose_name_plural = "天气"
        ordering = ['currentCity']