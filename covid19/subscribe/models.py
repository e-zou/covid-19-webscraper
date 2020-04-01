from django.db import models
from localflavor.us.models import USStateField

class Subscription(models.Model):
    email = models.EmailField(max_length=200)
    state = USStateField()
    validated = models.BooleanField(default=False)