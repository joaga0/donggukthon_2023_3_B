from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views

app_name = 'badge'

urlpatterns = [
    path('', views.badge_list),
    path('<int:badge_id>', views.acquired_badge),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

