from django import forms
from django.forms import Textarea
from .models import Post



class CommentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
          'content': Textarea(attrs={'rows':4, 'cols':20}),
        }


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']