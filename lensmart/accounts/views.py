from pyexpat import model
from django.shortcuts import render
from audioop import reverse
from django.contrib import messages
from django.contrib.auth.models import auth, User
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from home.models import Customer

# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login.html')
    return render(request, 'login.html')

    # else:
    #     return render(request, '/')
  
def register(request):        
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['username']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'an account with this email already exists, please choose another email')
                return redirect('register.html')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                # customer_new, created = User.objects.get_or_create(order=order, product=product)
                customer_add = Customer(customer = user,name=(first_name+last_name),email=email)
                customer_add.save()
                return redirect('login.html')
        else:
            messages.info(request,'your password\'s did not match')
            return redirect('register.html')
    else:
        return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect('/')