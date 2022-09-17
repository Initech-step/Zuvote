
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import secrets

# Create your views here.

def index(request):
    return render(request, 'general/prime.html')
