from django import forms
from django.forms import TextInput, Textarea

from Blog.models import Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': TextInput(attrs={'data-role': 'popover', 'data-popover-text': 'Max 64 characters'}),
            'content': Textarea(attrs={'data-role': 'popover', 'data-popover-text': 'Max 2048 characters', 'rows': 15}),
        }
