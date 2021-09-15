from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.forms import ModelForm
# Create your views here.


def index(request):
    context = {
        'sells': Item.objects.all()
    }
    return render(request, 'index.html', context)
