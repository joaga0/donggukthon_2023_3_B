from django.urls import path
from .views import *
from . import views

app_name = 'charity'
urlpatterns = [
    path('', views.charity_list),
    path('<int:id>', views.charity_detail),
]