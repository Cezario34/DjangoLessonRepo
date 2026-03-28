from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import HabitForm
from .models import Habit, HabitLog


# Create your views here.

@login_required
def habit_list(request):
    habits = Habit.objects.filter(is_active=True)
    today = timezone.localdate()
    completed_today_ids = set(
        HabitLog.objects.filter(
            date=today,
            is_completed=True,
            habit__is_active=True,
            ).values_list('habit_id', flat=True),
        )
    habit_cards = []
    for habit in habits:
        if habit.target_period == 'week':
            period_days = 7
        else:
            period_days = 30

        start_date = today - timedelta(days=period_days - 1)
        habit_start = habit.created_at.date()
        start_date = max(start_date, habit_start)

        logs = HabitLog.objects.filter(
            habit=habit,
            date__range=[start_date, today],
            is_completed=True,
            )
        completed_dates = set(logs.values_list('date', flat=True))
        completed_count = len(completed_dates)

        percent = min(
            round((completed_count / habit.target_count) * 100),
            100,
            ) if habit.target_count else 0

        weekday_map = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

        calendar_days = []
        for i in range(period_days):
            day = start_date + timedelta(days=i)
            calendar_days.append(
                {
                    'date': day,
                    'weekday': weekday_map[day.weekday()],
                    'is_completed': day in completed_dates,
                    'is_today': day == today
                    },
                )
        habit_cards.append(
            {
                'habit': habit,
                'percent': percent,
                'calendar_days': calendar_days,
                'is_completed_today': habit.id in completed_today_ids,
                },
            )

    return render(
        request,
        'tracker/habit_list.html',
        {
            'habit_cards': habit_cards,
            'today': today,
            },
        )


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tracker:habit_list'))
    else:
        form = HabitForm()
    return render(request, 'tracker/habit_form.html', {'form': form})


@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)

    if request.method == 'POST':
        habit.delete()
        return HttpResponseRedirect(reverse('tracker:habit_list'))
    return render(
        request,
        'tracker/habit_confirm_delete.html',
        {'habit': habit},
        )


@login_required
def habit_update(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tracker:habit_list'))
    else:
        form = HabitForm(instance=habit)

    return render(
        request,
        'tracker/habit_form.html',
        {
            'form': form,
            'habit': habit,
            'is_edit': True,
            },
        )


@login_required
def habit_toggle(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, is_active=True)
    today = timezone.localdate()
    log, created = HabitLog.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'is_completed': True},
        )

    if not created:
        log.is_completed = not log.is_completed
        log.save()

    return redirect('tracker:habit_list')
