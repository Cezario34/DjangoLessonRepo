from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('add/', views.habit_create, name='habit_create'),
    path('toggle/<int:habit_id>/', views.habit_toggle, name='habit_toggle_today'),
    path('edit/<int:habit_id>/', views.habit_update, name='habit_update'),
    path('delete/<int:habit_id>/', views.habit_delete, name='habit_delete'),
]

