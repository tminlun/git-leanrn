# Generated by Django 2.0 on 2018-10-18 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog1', '0010_auto_20181016_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readnum',
            name='blog',
        ),
        migrations.DeleteModel(
            name='ReadNum',
        ),
    ]
