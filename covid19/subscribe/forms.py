from django import forms
from localflavor.us.forms import USStateSelect
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Subscription

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('email', 'state',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
