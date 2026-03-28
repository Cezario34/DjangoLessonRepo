from .models import Comment, Post
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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',  'body', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок'}),
            'body': forms.Textarea(attrs={'placeholder': 'Текст поста', 'rows': 10}),
            'status': forms.Select(),
        }