from django.contrib import admin
from .models import BlogType,Blog1

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name',)
    ordering = ['id',]


@admin.register(Blog1)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','blog_type','get_read_num','contents','created_time','last_updated_time',)

