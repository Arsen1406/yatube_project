from django import forms
from . models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            'text': 'Текст поста',
            'group': 'Группы',
        }
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
        }
        help_text = {
            'text': ('Обязательное поле, не должно быть пустым')
        }
