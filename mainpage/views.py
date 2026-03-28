from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from blog.models import Post
from tracker.models import Habit, HabitLog
from tasks.models import Task

# Create your views here.
@login_required
def welcome(request):
    today = timezone.localdate()

    latest_posts = Post.published.order_by('-publish').first()

    completed_today_ids = set(
        HabitLog.objects.filter(
            date=today,
            is_completed=True,
            habit__is_active=True
            ).values_list('habit_id', flat=True)
        )
    tasks = Task.objects.filter(
        is_completed=False,
        period='day'
    ).order_by('due_date', '-created_at')

    open_habits = Habit.objects.filter(is_active=True).exclude(id__in=completed_today_ids)
    return render(request, 'welcome/start.html',
                  {'current_date': timezone.now().date(),
                      'latest_post': latest_posts,
                      'open_habits': open_habits,
                      'tasks': tasks})
