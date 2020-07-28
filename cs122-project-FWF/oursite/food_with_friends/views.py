import json
import traceback
import sys
import csv
import os
import re
import crawler
import database
import algorithm
import pandas as pd
from functools import reduce
from operator import and_
from .models import Group, Preferences

from django.shortcuts import render
from django import forms

from django.shortcuts import redirect
from django.core.validators import RegexValidator
from django.views.generic.edit import FormView
from django.core.validators import MaxValueValidator, MinValueValidator
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#TO DO
#find a way of linking homepage to form for each response
#home page should take address information and number of people and 
#create a new page where the first person and everyone else included


RANGE_WIDGET = forms.widgets.MultiWidget(widgets=(forms.widgets.NumberInput,
                                                  forms.widgets.NumberInput))

class InitSearchForm(forms.Form):
    street_address = forms.CharField(
            label='Street Address',
            help_text='Make sure address starts with a number.',
            error_messages={'incomplete': 'Enter a street address.'},
            validators=[RegexValidator(regex = r'^[0-9]', message = 'Enter a valid country calling code.')],
            required = True)
    city = forms.CharField(
            label='City',
            help_text='Enter a city name using only English letters.',
            error_messages={'incomplete': 'Enter a city name, only using English letters.'},
            validators=[RegexValidator(regex = r'^[a-zA-Z]+$', message = 'Enter a valid city name.')],
            required = True)
    state = forms.CharField(
            label='State Code',
            help_text='Enter two letter abbreviation for state.',
            validators=[RegexValidator(regex = r'^(?:(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY]))$', message = 'Enter a valid valid 2 digit state code in capital letters.')],
            error_messages={'incomplete': 'Use only two capital letterusing letters.'},
            required = True)
    delivery_max = forms.CharField(
             label='Delivery Time Maximum',
             help_text='Enter a number between 15-99.')
    people = forms.IntegerField(
            label = 'How many people want to order food?',
            help_text = 'Enter a number between 1 and 10.',
            validators=[MaxValueValidator(10), MinValueValidator(1)],
            error_messages = {'incomplete': 'Enter a number between 1 and 10.'}
        )
class FoodPreferenceForm(forms.Form):
    query = forms.CharField(
            label='What food you want to eat?',
            help_text='Enter a dish you would like to eat,',
            error_messages={'incomplete': 'Enter whatever you want to eat'},
            max_length = 100
            )
    strength = forms.ChoiceField(
            label='How strong is this preference?',
            choices = [(2,'strong'), (1,'normal'), (.5,'weak')])
    budget = forms.IntegerField(
    	label = 'What is the most you are willing to spend?',
    	help_text = 'Enter a number between 0 and 100.',
    	validators=[MaxValueValidator(100), MinValueValidator(1)],
    	error_messages = {'incomplete': 'Enter a number between 1 and 10.'}
    	)   
class NameForm(forms.Form):
    name = forms.CharField(
            label='Your name',
            help_text='Enter your name, only use english letters',
            error_messages={'incomplete': 'Enter your name.'},
            required = True,
            validators=[RegexValidator(regex = r'^[a-zA-Z]+$', message = 'Only use english letters.')],
            )
class WaitButton(forms.Form):
	button = forms.Select(choices = ('Everyone is ready', 'Everyone is ready'),
	 )

def home(request):
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = InitSearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # Convert form data to an args dictionary for find_courses
            # group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name = group_code)
            address = form.cleaned_data['street_address'] + " " + \
                            form.cleaned_data['city'] + ", " + \
                            form.cleaned_data['state']
            group = Group(address=address, 
                          name_count = 0, num_people=form.cleaned_data['people'],
                          p_tables = 0,
                          delivery_time_max=form.cleaned_data['delivery_max'],
                          conversion = '0')
            group.save()
            return HttpResponseRedirect(str(group.group_id))
    else:
        form = InitSearchForm()     
    return render(request, 'index.html', {'form': form})


def namepage(request, code):
    group_id = str(code)
    if request.method == 'GET':
        form = NameForm(request.GET)
        if form.is_valid():
            g = Group.objects.get(group_id=str(group_id))
            g.name_count += 1
            pref = Preferences(name=form.cleaned_data['name'], group=g.group_id,
                               individual=g.name_count, strength_of_pref = 0.0,
                               budget = 0)
            g.save()
            pref.save()
            return HttpResponseRedirect(str(g.name_count))
    else:
        form = NameForm(request.GET)
    return render(request, 'name.html', {'form': form})


def prefs(request, code, individual):
    group_id = code
    if request.method == 'GET': 
        form =  FoodPreferenceForm(request.GET)
        if form.is_valid():
            p = Preferences.objects.get(group = group_id, individual = individual)
            g = Group.objects.get(group_id = group_id)
            p.strength_of_pref = float(form.cleaned_data['strength'])
            p.food_preference = form.cleaned_data['query']
            p.budget = form.cleaned_data['budget']
            g.p_tables += 1
            p.save()
            g.save()
            if g.p_tables == g.num_people:
                return HttpResponseRedirect("/"  + str(code) + '/final/')
            else:
                return HttpResponseRedirect('/'  + str(code) + '/wait/')
    else:
        form = FoodPreferenceForm(request.GET)
    return render(request, 'index.html', {'form': form})

def wait(request, code):
    g = Group.objects.get(group_id=code)
    if g.conversion != '0':
    	return HttpResponseRedirect("/"  + str(code) + '/final/')
    num_left = g.num_people - g.p_tables
    if request.method == 'GET':
    	form = WaitButton(request.GET)
    	if form.is_valid:
    		HttpResponseRedirect('/'  + str(code) + '/wait/')
    return render(request, 'index.html', {'form': form})

def final(request, code):
    names = []
    inputs = {"people": {}}
    if request.method == 'GET':
        g = Group.objects.get(group_id = code)
        if g.conversion != '0':
        	return render(request, 'final.html',{'results': g.conversion} )
        lst = Preferences.objects.filter(group = code)
        tuple_dict = crawler.go(g.address)
        rest_db, menu_db = database.get_pandas(tuple_dict)
        for person in lst:
            inputs["people"][person.individual] = [person.food_preference]
            inputs["people"][person.individual] += [person.strength_of_pref]
            inputs["people"][person.individual] += [person.budget]
            names.append(person.name)
        inputs["delivery_time"] = g.delivery_time_max
        results = algorithm.calc_score(rest_db, menu_db, inputs, names)
        conversion = pd.DataFrame.to_html(results, header = True, escape = False, bold_rows = True, justify = 'center')
        conversion.replace('\n', '')
        g.conversion = conversion
        g.save()
    return render(request, 'final.html',{'results': conversion} )
