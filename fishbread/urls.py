from django.urls import path
from .views import *
from . import views

app_name = 'fishbread'
urlpatterns = [
    path('fishbread/', views.fishbread_info),
    path('fishbread/<int:id>', views.fishbread_detail),
]