from .models import Task
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'period']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название таски'}),
            'description': forms.TextInput(attrs={'placeholder': 'Описание задачи'}),
            'due_date': forms.TextInput(attrs={'placeholder': 'Дедлайн'}),
            }