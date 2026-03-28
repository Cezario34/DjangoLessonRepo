from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from tasks.models import Task
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


@login_required
def task_list(request):
    selected_period = request.GET.get('period', 'all')
    active_tasks = Task.objects.filter(is_completed=False)
    completed_tasks = Task.objects.filter(is_completed=True)

    if selected_period != 'all':
        active_tasks = active_tasks.filter(period__icontains=selected_period)
        completed_tasks = completed_tasks.filter(period__icontains=selected_period)

    return render(
        request,
        'task/task_list.html',
        {
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
        }
    )

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return HttpResponseRedirect(reverse('tasks:task_list'))
    else:
        form = TaskForm()

    return render(request,
                  'task/create_task.html',
                  {'form':form})


@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return HttpResponseRedirect(reverse('tasks:task_list'))
    else:
        form = TaskForm(instance=task)

    return render(request, 'task/task_update.html', {'form':form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect(reverse('tasks:task_list'))
    return render(
        request,
        template_name='task/delete_task.html',
        context={'task':task}
        )

@login_required
def task_toggle_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('tasks:task_list')