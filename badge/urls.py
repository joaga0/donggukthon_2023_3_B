from django.urls import path
from .views import *
from . import views

app_name = 'badge'
urlpatterns = [
    path('', views.badge_list),
    path('<int:id>', views.acquired_badge),
]