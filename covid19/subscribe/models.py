from django.db import models
from localflavor.us.models import USStateField

class Subscription(models.Model):
    email = models.CharField(max_length=200)
    state = USStateField()
