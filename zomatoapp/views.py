from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import *
import requests
from django.http import HttpResponseRedirect

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
    if queryset:
        resturant = Resturant.objects.filter(city__icontains=queryset)
    else:
        resturant = Resturant.objects.all()
    category = Category.objects.all()[:4]
    context={
        'resturant':resturant,
        'category': category
     
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

def detail(request,resturantid):
    resturant = Resturant.objects.filter(id=resturantid)
    category = Category.objects.all()
    dish = None
    category_id = request.GET.get('category')
    if category_id:
        dish = Dish.Dishbycategories(categoryid=category_id,resturantname=resturant)
    else:
        dish = Dish.objects.filter(resturant__name__contains=resturant.first())
    context = {
        'resturant' : resturant,
        'category' : category,
        'dish' : dish
    }
    return render(request,"detail.html",context=context)


import razorpay
client = razorpay.Client(auth=("rzp_test_FVgxuzBdJ9c4So", "4riLfbUSnTNTzkNFzoIqA7GD"))

@login_required
def buy(request,dish_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('/login')    
    dish = Dish.objects.get(id=dish_id)
    order_amount = dish.price * 100
    order_currency = 'INR'
    order_receipt = 'order_rcptid_{dish.id}_{user.id}'
    data = {
        'amount' : order_amount,
        'currency' : order_currency,
        'receipt' : order_receipt
    }
    order = client.order.create(data=data)
    payment = Payment(user=user,dish=dish,status='fail',order_id=order.get('id'))
    payment.save()
    print(order)
    context={
        'dish':dish,
        'order': order
    }

    return render(request,"buy.html",context) 


def orders(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
    else:
        user = None    
    userproduct = Userproduct.objects.filter(user=user)

    context = {
        'userproduct' : userproduct
    }        

    return render(request,"order.html",context=context)

@csrf_exempt
def verifypayment(request):
    if request.method == "POST":
        print(request.POST)
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id = razorpay_order_id)
        payment.status = "success"
        payment.payment_id = razorpay_payment_id
        payment.save()

        user_product = Userproduct(user = payment.user,payment=payment,dish=payment.dish)
        user_product.save()
        return redirect ('/orders')
