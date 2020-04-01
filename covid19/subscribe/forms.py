from django import forms
from localflavor.us.forms import USStateSelect
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Subscription
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

# Help from: https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('email', 'state',)

    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'subscribeForm'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Subscribe')
        )

class UnsubscribeForm(forms.Form):
    email = forms.CharField(label='email', max_length=100)

    def __init__(self, *args, **kwargs):
        super(UnsubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'unsubscribeForm'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit'),
        )