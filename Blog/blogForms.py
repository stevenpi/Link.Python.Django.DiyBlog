from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, Textarea, FileInput
from django.utils.translation import ugettext_lazy as _

from Blog.models import Post, Profile


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': TextInput(),
            'content': Textarea(attrs={'rows': 15}),
        }

        labels = {
            'title': _('Title'),
            'content': _('Content')
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

        labels = {
            'email': _('Email'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

        labels = {
            'bio': _('Bio'),
            'image': _('Image'),
        }

        widgets = {
            'image': FileInput(attrs={'data-role': 'file', 'dir': 'rtl'}),
        }

