#File: forms.py
#Author: Niyoo Nedi (nnedi@bu.edu), 4/20/2026
#Description: File that contains the forms for my final project

from django import forms
from .models import Booking
from allauth.account.forms import SignupForm

class BookingForm(forms.ModelForm):
    '''Form for creating a booking'''

    def __init__(self, *args, **kwargs):
        '''Initializes the form'''
        #pop the rooms from the kwargs
        rooms = kwargs.pop("rooms", None)
        #call the super class to initialize the form
        super().__init__(*args, **kwargs)

        #if the rooms are not None, set the queryset for the room field to the rooms
        if rooms is not None:
            #set the queryset for the room field to the rooms passed in
            self.fields["room"].queryset = rooms

    class Meta:
        model = Booking
        #fields for the form
        fields = ["room", "start_time", "end_time"]

        #widgets for the form
        widgets = {
            #widget for the start time field
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            #widget for the end time field
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class CustomSignupForm(SignupForm):
    '''Custom signup form that only allows BU emails'''

    def clean_email(self):
        '''Cleans the email'''
        #get the email from the cleaned data
        email = self.cleaned_data.get("email")

        #if the email is not provided, raise a validation error
        if not email:
            raise forms.ValidationError("Email is required.")

        #if the email does not end with @bu.edu, raise a validation error
        if not email.endswith("@bu.edu"):
            raise forms.ValidationError("Only BU emails are allowed.")

        return email