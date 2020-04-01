from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mass_mail
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .forms import SubscribeForm, UnsubscribeForm
from .models import Subscription


def index(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.email = form.cleaned_data['email']
            form.state = form.cleaned_data['state']
            form.save()
            return redirect('/') # clears form
    else:
        form = SubscribeForm()
    return render(request, 'index.html', {'form': form})


def thanks(request):
    return HttpResponse("Thank you! You have been subscribed.")


# TO-DO: wait until the person has gotten an email to unsubscribe
def unsubscribe(request):
    form = UnsubscribeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form_email = form.cleaned_data['email']
            if (Subscription.objects.filter(email = form_email).exists()):
                subscription = Subscription.objects.filter(email = form_email)
                for s in subscription:
                    s.delete()
                return redirect('/')

    return render(request, 'unsubscribe.html', {'form': form})