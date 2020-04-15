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

import bs4
import requests
from bs4 import BeautifulSoup as soup
from datetime import date

import schedule
import time

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
            validateEmail(form.email)
            send_mail(
                'COVID-19 Case Count Subscription',
                'Thank you for subscribing. You will start getting case count emails every day at 7a.m. :)',
                'ashmilyz@gmail.com',
                [form.email],
                fail_silently=False,
            )
            return redirect('thanks') # clears form
    else:
        form = SubscribeForm()
    return render(request, 'index.html', {'form': form})

#TO-DO: make a pop up modal or page for the thank you 
def thanks(request):
    return render(request, 'thanks.html')


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
                send_mail(
                    'Unsubscribed',
                    'Sorry to see you unsubscribe! Let us know if you have any feedback. :)',
                    'ashmilyz@gmail.com',
                    [form_email],
                    fail_silently=False,
                )
                return redirect('/')

    return render(request, 'unsubscribe.html', {'form': form})


# TO-DO: https://www.youtube.com/watch?v=A-7vGF_pEss
# TO-DO: scrape data off of https://www.worldometers.info/coronavirus/country/us/
def getData(): 

    my_url = "https://www.worldometers.info/coronavirus/country/us/"
    my_r = requests.get(my_url)
    page_soup = soup(my_r.content, "html.parser")
    state_table = page_soup.find("table", {"id": "usa_table_countries_yesterday"}).tbody
    state_table_rows = state_table.find_all('tr')

    all_subs = Subscription.objects.all()

    for sub in all_subs:
        sub_email = sub.email
        sub_state = sub.state
        sub_state = abbrev_us_state[sub_state]
        # print(sub_email + ", " + sub_state)
        for state_row in state_table_rows:
            cols = state_row.find_all('td')
            state_name = cols[0].string.strip()
            print(state_name)
            if(sub_state == state_name):
                print("Found match!" + sub_state + " and " + state_name)
                total_cases = cols[1].string.strip()
                new_cases = cols[2].string.strip()
                total_deaths = cols[3].string.strip()
                new_deaths = cols[4].string.strip()
                active_cases = cols[5].string.strip()
                if (total_cases == ""):
                    total_cases = "0"
                if (new_cases == ""):
                    new_cases = "0"
                if (total_deaths == ""):
                    total_deaths= "0"
                if (new_deaths == ""):
                    new_deaths = "0"
                if (active_cases == ""):
                    active_cases = "0"
                #send email function
                # message = "Today, " + state_name + " has " + total_cases + " total cases.\nNew cases: " + new_cases + "\nTotal deaths: " + total_deaths + "\nNew deaths: " + new_deaths + "\nActive cases: " + active_cases + ""

                # send_mail(
                #     'COVID-19 Daily Update',
                #     message,
                #     'ashmilyz@gmail.com',
                #     [sub_email],
                #     fail_silently=False,
                # )
                # print('Sent email!')

                today = date.today().strftime("%B %d, %Y")
                subject = total_cases + "Total Cases in " + sub.state + "| Daily COVID-19 Update" 
                message = today + " | " + state_name + "\nTotal cases " + total_cases + " total cases.\nNew cases: " + new_cases + "\nTotal deaths: " + total_deaths + "\nNew deaths: " + new_deaths + "\nActive cases: " + active_cases + ""

                send_mail(
                    subject,
                    message,
                    'ashmilyz@gmail.com',
                    [sub_email],
                    fail_silently=False,
                )

def job(): 
    print("job")
   
# schedule.every(5).minutes.do(getData)
schedule.every().second.do(job)
# schedule.every().day.at("17:38").do(getData)


while True:
    schedule.run_pending()
    time.sleep(1)
   


us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# thank you to @kinghelix and @trevormarburger for this idea
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))