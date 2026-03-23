from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
            'body': forms.Textarea(attrs={'placeholder': 'Напишите комментарий...'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(label = 'Поиск', max_length = 100)