from django import forms
from django.core.exceptions import ValidationError

from news.models import Subscribers


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email', ]


class ContactForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=10)
    email = forms.EmailField()
    msg = forms.CharField()

    def clean_msg(self):
        data = self.cleaned_data['msg']
        print(data)
        raise ValidationError("msg has no valid words")

    def clean(self):
        data = self.cleaned_data
