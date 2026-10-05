#File: adapters.py
#Author: Niyoo Nedi (nnedi@bu.edu), 4/19/2026
#Description: File that contains the adapter for user account creaiton

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import redirect

class BUOnlyAdapter(DefaultSocialAccountAdapter):
    '''Custom adapter for django-allauth that restricts authentication to users with a BU email'''

    def pre_social_login(self, request, sociallogin):
        '''Func that runs just before a social login is completed'''

        email = sociallogin.user.email
        if not email.endswith("@bu.edu"):
            
            messages.error(request, "Only BU Google accounts are allowed.")
            raise ImmediateHttpResponse(redirect("/accounts/login/"))
        

