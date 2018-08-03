from django.urls import path
from . import views

urlpatterns = [
	#博客首页
	path('',views.blog_list, name="blog_list"),
    path('<int:blog_pk>',views.blog_detail, name="blog_detail"),
    path('type/<int:type_pk>',views.blogs_with_type, name="blogs_with_type"),

]