# Generated by Django 2.0 on 2018-10-10 04:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog1', '0003_remove_blog1_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog1',
            name='content',
            field=ckeditor.fields.RichTextField(default=0),
        ),
    ]
