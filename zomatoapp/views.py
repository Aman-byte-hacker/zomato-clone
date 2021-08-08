from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import *
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

def search(request):
    queryset = request.GET.get('query')
    resturant = Resturant.objects.filter(city__icontains=queryset)

    context={
        'resturant':resturant,
     
    }    
    print(queryset)
    return render(request,"search.html",context=context)

def searchresturant(request):
    resturant = request.GET.get('rest')
    resturants = Resturant.objects.filter(name__icontains=resturant)
    dishes = Dish.objects.filter(name__icontains=resturant)
    context = {
        'resturants' : resturants,
        'dish' : dishes
    }
    print(resturant)
    return render(request,"searchrest.html",context=context)