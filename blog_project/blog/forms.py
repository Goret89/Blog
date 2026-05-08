from django import forms
from .models import Post
from .models import Comment, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ['author', 'content']
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'class': 'form-control', 'placeholder': 'Leave a comment...'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
