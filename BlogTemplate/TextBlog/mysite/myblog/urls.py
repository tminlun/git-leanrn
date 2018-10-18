from django.urls import path
from . import views

urlpatterns = [
    path('fengmian/', views.fengmian, name="fengmian"),
    path('time/', views.time, name="time"),
    path('', views.index, name="index"), #index,博客列表
    path('<int:blog_pk>',views.info,name="info"), #博客细节
    path('picture/',views.picture, name="picture"),
    path('type/<int:type_pk>', views.blog_type, name="blog_type"),
    # path('date/<int:year>/<int:month>', views.blog_date, name="blog_date"),
]


