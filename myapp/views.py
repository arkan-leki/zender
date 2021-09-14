from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    context = {
        'sells': Item.objects.all()
    }
    return render(request , 'index.html' , context)