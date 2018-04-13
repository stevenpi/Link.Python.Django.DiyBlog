from django import forms
from django.forms import TextInput, Textarea
from django.utils.translation import ugettext_lazy as _

from Blog.models import Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': TextInput(attrs={'data-role': 'popover', 'data-popover-text': _('Max 64 characters'), }),
            'content': Textarea(attrs={'data-role': 'popover', 'data-popover-text': _('Max 2048 characters'), 'rows': 15}),
        }

        labels = {
            'title': _('Title'),
            'content': _('Content')
        }
