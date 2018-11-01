from django.contrib import admin
from .models import BlogType,Blog,Blog_with_news

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id','type_name',]
    ordering = ['id',]

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','blog_type','get_read_num','contents','created_time','last_time']


@admin.register(Blog_with_news)
class Blog_with_news_Admin(admin.ModelAdmin):
    list_display = ['title','author','blog_type','reader_num','content','created_time','last_time',]