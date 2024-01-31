from .models import *
from rest_framework import serializers


class SupplierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Suppliers
        fields = "__all__"


class BuyerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Buyers
        fields = "__all__"

class OrdersReceivedSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdersReceived
        fields = "__all__"

class OrdersSentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdersSent
        fields = "__all__"