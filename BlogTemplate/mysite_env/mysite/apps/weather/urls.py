from django.urls import path
from . import views


urlpatterns = [
    #总首页
    path('', views.weather, name="weather"),
    path('weather-api/', views.weather_api, name="weather-api"),
]