from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse

from application.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth import authenticate, login

# Create your views here.

class loginPage(TemplateView):
    template_name = "login.html"

def login_auth(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        response =  HttpResponseRedirect(reverse('application:create_case'))
        return response
    else:
        messages.error(request, 'Incorrect username/password!')
        return HttpResponseRedirect(reverse('application:login_page'))