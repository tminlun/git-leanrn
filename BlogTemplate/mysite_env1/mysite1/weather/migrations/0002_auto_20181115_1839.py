# Generated by Django 2.0 on 2018-11-15 10:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weather',
            options={'verbose_name': '天气', 'verbose_name_plural': '天气'},
        ),
        migrations.AlterField(
            model_name='weather',
            name='Picture',
            field=models.ImageField(upload_to='', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='currentCity',
            field=models.CharField(max_length=10, verbose_name='城市名'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='data',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='日期'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='pm25',
            field=models.CharField(max_length=10, verbose_name='PM25'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='the_weather',
            field=models.TextField(verbose_name='气候'),
        ),
    ]