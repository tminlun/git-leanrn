from django.contrib import admin
from .models import Weather

# Register your models here.

@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('today_or_future', 'currentCity', 'pm25', 'data', 'Picture','temperature','the_weather')

