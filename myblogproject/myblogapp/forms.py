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
        fields = ["title", "content", "topic"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목"}),
            "content": SummernoteWidget(),
            "topic": forms.RadioSelect(
                choices=[
                    ("daily", "일상"),
                    ("cooking", "요리"),
                    ("trip", "여행"),
                    ("movie", "영화"),
                    ("IT", "IT / 전자기기"),
                ],
                attrs={"class": "topic-option"},
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["topic"].required = False


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = False
        self.fields['publish'].required = False
        self.fields['views'].required = False