from django.contrib import admin
from .models import ReadNum,ReadNumDate

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_object') # content_type别的模型的名称

@admin.register(ReadNumDate)
class ReadNumDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')
