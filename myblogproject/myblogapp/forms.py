from django import forms
from .models import Article

from django_summernote.widgets import SummernoteWidget


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'login-input'}),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-input'}),
        label='',
    )

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["content"]
        widgets = {
            "content": SummernoteWidget(),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = False
        self.fields['publish'].required = False
        self.fields['views'].required = False