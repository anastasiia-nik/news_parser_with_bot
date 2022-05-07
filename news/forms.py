from django.core.exceptions import ValidationError

from .models import Comment
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class SampleForm(forms.Form):
    text = forms.CharField(max_length=100)

class CommentForm(forms.ModelForm):
    # captcha = ReCaptchaField()
    class Meta:
        model = Comment
        fields = ('author', 'text')
        # exclude = ['date', 'news_id', 'approved']
        # captcha = ReCaptchaField()

class Comment2Form(forms.Form):
    author = forms.CharField(min_length=1, max_length=100)
    text = forms.CharField(min_length=3, max_length=1024)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context')
        super().__init__(*args, **kwargs)

    def clean_author(self):

        return self.cleaned_data['author']

    # def clean_text(self):
    #     request = self.context['request']
    #     if request.user.is_superuser:
    #         return
    #
    #     m = self.cleaned_data['msg']
    #     if 'Зеленский' in m:
    #         raise ValidationError("dasdad")
    #

    def clean(self):
        data = self.cleaned_data
        if Comment.objects.filter(author=data['author'], text=data['text']).exists():
            raise ValidationError("такое уже есть!")
