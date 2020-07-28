from django.shortcuts import render

from django.http import HttpResponse
from django.core.validators import RegexValidator
from django import forms

import re

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class AddressFields(MultiValueField):
    def __init__(self, **kwargs):
        error_messages = {'incomplete':
        'Enter street address, city and state'}
        fields = (
            CharField(
                label='Street Address',
                help_text='Make sure address starts with a number.',
                error_messages={'incomplete': 'Enter a street address.'},
                validators=[
                    RegexValidator(r'^[0-9]', 'Enter a valid country calling code.'),
                ],
            ),
            CharField(
                label='City',
                help_text='Enter a city name using only English letters.',
                error_messages={'incomplete': 'Enter a city name, only using English letters.'},
                validators=[RegexValidator(r'^[a-zA-Z]+$', 'Enter a valid city name.')],
            ),
            CharField(
                label='State Code',
                help_text='Enter two letter abbreviation for state.',
                validators=[RegexValidator(r'^(?-i:A[LKSZRAEP]|C[AOT]|D[EC]|F[LM]|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEHINOPST]|N[CDEHJMVY]|O[HKR]|P[ARW]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])$', 'Enter a valid valid 2 digit state code in capital letters.')],
                error_messages={'incomplete': 'Use only two capital letterusing letters.'},
            ),
            CharField(
                label='Delivery Time',
                help_text='Enter a number between 0-99',
                validators=[RegexValidator('^[0-9]{2}', 'Enter a number between 0 and 99')],
                error_messages={'incomplete': 'Enter a number, eg 64, between 0 and 99.'},
            ),
        )
        super().__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=True, **kwargs)
class PreferenceForm(MultiValueField):
    def __init__(self, **kwargs):
        fields = (
            CharField(
                label='What do you want to eat?',
                help_text='Enter what you want to eat. Use only one word with only English letters',
                error_messages={'incomplete': 'Enter one word, you can add multiple preferences but each must be one word consisting of only English Letters'},
                validators=[RegexValidator(r'^[a-zA-Z]+$', 'Enter a valid preference.'),],
                ),
            ChoiceField(
                label='How strong is this preference?',
                choices = ['strong','medium','low']
                )   
            )
        