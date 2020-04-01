from django.conf import settings
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
from django.core.mail import BadHeaderError, send_mail

from .forms import SubscribeForm, UnsubscribeForm
from .models import Subscription

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def index(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.email = form.cleaned_data['email']
            form.state = form.cleaned_data['state']
            form.save()
            # validateEmail(form.email)
            emailArr = []
            emailArr.append(form.email)
            send_mail(
                'COVID-19 Case Count Subscription',
                'Thank you for subscribing. You will start getting case count emails every day at 7a.m. :)',
                'ashmilyz@gmail.com',
                [form.email],
                fail_silently=False,
            )
            return redirect('/') # clears form
    else:
        form = SubscribeForm()
    return render(request, 'index.html', {'form': form})

#TO-DO: make a pop up modal or page for the thank you 
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


# TO-DO: https://www.youtube.com/watch?v=A-7vGF_pEss
# TO-DO: scrape data off of https://www.worldometers.info/coronavirus/country/us/