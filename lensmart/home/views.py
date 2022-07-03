from audioop import reverse
import json
from multiprocessing import context
from urllib import request
from django.contrib.auth.models import auth, User
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from django.http import JsonResponse
import datetime
# Create your views here.
def home(request):
    if request.method=="POST":
        email_sub = request.POST['email_sub']
        email_sub = Subscription(email_sub=email_sub)
        email_sub.save()
    return render(request, 'index.html')

def about(request):
    if request.method=="POST":
        email_sub = request.POST['email_sub']
        email_sub = Subscription(email_sub=email_sub)
        email_sub.save()
    return render(request, 'about.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products':products})

def contact(request):
    if request.method=="POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contacts = Contact(fullname=fullname, email=email, phone=phone, message=message)
        contacts.save()
    return render(request, 'location.html')

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

def mycart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'mycart.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
    print('Data',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if order.shipping == True:
            ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			pincode=data['shipping']['pincode'],
			)
        if total == order.get_cart_total:
            order.complete = True
        order.save()
    return JsonResponse('Payment submitted..', safe=False)