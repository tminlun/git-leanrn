# Generated by Django 2.0 on 2018-10-26 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0003_readnum_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readnumdate',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='ReadNumDate',
        ),
    ]
