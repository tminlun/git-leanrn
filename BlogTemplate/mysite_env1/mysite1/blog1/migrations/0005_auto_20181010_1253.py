# Generated by Django 2.0 on 2018-10-10 04:53

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog1', '0004_blog1_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog1',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
