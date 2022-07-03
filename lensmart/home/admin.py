from email import message
from django.contrib import admin
from .models import *
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'phone', 'message']
admin.site.register(Product)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Subscription)
admin.site.register(ShippingAddress)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
