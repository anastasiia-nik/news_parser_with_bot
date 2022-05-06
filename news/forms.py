from captcha.widgets import ReCaptchaV3

from .models import Comment
from django import forms
from captcha.fields import ReCaptchaField


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        # exclude = ['date', 'news_id', 'approved']
        captcha = ReCaptchaField(widget=ReCaptchaV3)


