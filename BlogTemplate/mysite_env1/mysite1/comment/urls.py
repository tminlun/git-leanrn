from django.urls import path
from . import views

from django.conf import settings

urlpatterns = [
    path('update_comment/',views.update_comment, name="update_comment"),
]