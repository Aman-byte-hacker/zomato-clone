from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
import requests
import json

# Create your views here.

def index(request):
    location_data = requests.get("https://api.ipify.org?format=json")
    locationdata = json.loads(location_data.text)
    location = requests.get('http://ip-api.com/json/'+locationdata['ip'])
    locationuser = json.loads(location.text)
    context = {
        'location':locationuser
    }
    return render(request,"index.html",context=context)

def login(request):
    return render(request,"login.html")    

def logout(request):
    request.session.clear()
    return redirect("/")