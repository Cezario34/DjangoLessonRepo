from django.contrib import admin
from .models import Habit, HabitLog
# Register your models here.

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_count', 'target_period', 'is_active', 'created_at']
    list_filter = ['is_active', 'target_period', 'created_at']
    search_fields = ['title', 'description']

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'date', 'created_at']
    search_fields = ['habit__title']