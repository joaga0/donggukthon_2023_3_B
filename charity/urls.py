from django.urls import path
from .views import *
from . import views

app_name = 'charity'
urlpatterns = [
    path('charity', views.foundation_list),
    path('charity/<int:id>', views.foundation_detail),
]