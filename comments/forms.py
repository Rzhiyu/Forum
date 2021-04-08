from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'xxxa'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
