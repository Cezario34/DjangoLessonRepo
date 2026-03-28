from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]