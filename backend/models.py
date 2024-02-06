from django.db import models
# Create your models here.

class Buyers(models.Model):
    id = models.AutoField(primary_key=True)
    buyer_name = models.CharField(max_length=100,unique=True)
    contact = models.CharField(max_length=15, null= True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    buyer_detail = models.CharField(max_length=500)
    order_count = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Buyers'

class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=15, null= True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    supplier_detail = models.CharField(max_length=500)
    order_count = models.IntegerField(default=0)
    status=models.BooleanField(default=True)
    class Meta:
        db_table = 'Suppliers'

class OrdersReceived(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('authentication.User', verbose_name= "User", default=1, on_delete=models.SET_DEFAULT)
    buyer_id = models.ForeignKey("Buyers", verbose_name= "Buyers", default=1, on_delete=models.SET_DEFAULT)
    item_name = models.CharField(max_length = 200)
    item_quantity = models.IntegerField()
    item_cost = models.CharField(max_length =50, )
    date = models.DateField(null = True, blank = True)
    status = models.CharField(max_length =50, default='OrderReceived')
    purchase_order = models.FileField(upload_to='pdfs/',null = True, blank = True)
    invoice = models.FileField(upload_to='pdfs/',null = True, blank = True)
   
    class Meta:
        db_table = 'OrdersReceived_table'

class OrdersSent(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('authentication.User', verbose_name= "User", default=1, on_delete=models.SET_DEFAULT)
    supplier_id = models.ForeignKey("Suppliers", verbose_name= "Suppliers", default=1, on_delete=models.SET_DEFAULT)
    item_name = models.CharField(max_length = 200)
    item_quantity = models.IntegerField()
    item_cost = models.CharField(max_length =50, )
    date = models.DateField(null = True, blank = True)
    status = models.CharField(max_length =50, default='OrderPlaced')
    purchase_order = models.FileField(upload_to='pdfs/',null = True, blank = True)
    invoice = models.FileField(upload_to='pdfs/',null = True, blank = True)
   
    class Meta:
        db_table = 'OrdersSent_table'