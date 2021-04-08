from django import forms

from .models import Post, Category

choices = Category.objects.all().values_list('name', 'name')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'snippet', 'header_image', 'author', 'category', 'body')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your title here'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'xxxa', 'type': 'hidden'}),
            # 'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices, attrs={'class': 'form-control'}, ),
            'body': forms.Textarea(attrs={'class': 'form-control'}),

        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'snippet', 'header_image', 'category', 'body')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your title here'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('name', 'body')
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'xxxa', 'type': 'hidden'}),
#             'body': forms.Textarea(attrs={'class': 'form-control'}),
#         }
