from django.contrib import admin
from .models import Buyers, Suppliers, OrdersReceived, OrdersSent
# Register your models here.
admin.site.register(Buyers)
admin.site.register(Suppliers)
admin.site.register(OrdersReceived)
admin.site.register(OrdersSent)
