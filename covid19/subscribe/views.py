from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mass_mail
from django.utils.translation import gettext as _

from .forms import SubscribeForm
from .models import Subscription


def index(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.email = form.cleaned_data['email']
            form.state = form.cleaned_data['state']
            form.save()
            # redirects to the same page to clear the form
            # TO-DO: redirect to form
            return redirect('/subscribe')
    else:
        form = SubscribeForm()
    return render(request, 'index.html', {'form': form})


def thanks(request):
    return HttpResponse("Thank you! You have been subscribed.")
