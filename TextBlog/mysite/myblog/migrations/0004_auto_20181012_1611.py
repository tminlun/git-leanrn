# Generated by Django 2.0 on 2018-10-12 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_auto_20181011_2017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created_time']},
        ),
        migrations.AddField(
            model_name='blog',
            name='reader_num',
            field=models.IntegerField(default=0),
        ),
    ]
