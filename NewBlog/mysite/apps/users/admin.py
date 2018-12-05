from django.contrib import admin
from .models import UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserProfileAamin(admin.ModelAdmin):
    list_display = ('nick_name', 'brithday', 'gander')

