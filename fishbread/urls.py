from django.urls import path
from .views import *
from . import views

app_name = 'fishbread'
urlpatterns = [
    path('', views.fishbread_info),
    path('<int:id>', views.fishbread_detail),
]