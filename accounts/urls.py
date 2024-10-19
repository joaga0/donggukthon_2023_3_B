from django.urls import path, include
from . import views
from .views import *
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    # path('users/', UserListView.as_view(), name='user-list'),
    path('signup/', RegisterAPIView.as_view(), name='user-create'),
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/', PasswordChangeView.as_view(), name='password-change-done'),

    path('bank', UserBankViewSet.as_view(), name='bank'),
    path('mypage', UserViewSet.as_view(), name='mypage'),
    path('date', UserDateViewSet.as_view(), name='date'),
    path('fishbread', PasswordChangeDoneView.as_view(), name='fishbread')
]