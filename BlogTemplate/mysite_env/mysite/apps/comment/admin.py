from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):#content_object哪个博客
    list_display = ('content_object','context','comment_user','comment_time')
