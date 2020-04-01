from django import forms
from localflavor.us.forms import USStateSelect
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Subscription
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('email', 'state',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'subscribeForm'
        self.helper.add_input(Submit('submit', 'Subscribe'))