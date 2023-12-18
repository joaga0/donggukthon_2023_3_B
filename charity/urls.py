from django.urls import path
from .views import *
from . import views

app_name = 'fishbread'
urlpatterns = [
    path('', views.foundation_list),
    path('<int:id>', views.foundation_detail),
]