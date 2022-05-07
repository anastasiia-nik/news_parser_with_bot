from .models import Comment
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class SampleForm(forms.Form):
    text = forms.CharField(max_length=100)

class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Comment
        fields = ('author', 'text')
        # exclude = ['date', 'news_id', 'approved']
        # captcha = ReCaptchaField()


