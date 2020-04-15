from django.db import models
from localflavor.us.models import USStateField
from localflavor.us.us_states import US_STATES

class Subscription(models.Model):
    email = models.EmailField(max_length=200)
    state = USStateField(choices = US_STATES)
    validated = models.BooleanField(default=False)