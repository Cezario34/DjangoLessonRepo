from django import forms
from .models import Habit



class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'target_count', 'target_period']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название привычки'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описание', 'rows': 4}),
        }