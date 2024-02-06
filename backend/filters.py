import django_filters
from django_filters import rest_framework as filters
from .models import *
from .serializers import *

class BuyersFilters(filters.FilterSet):
    status = django_filters.BooleanFilter()
    buyer_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Buyers
        fields = {'buyer_name': ['exact','icontains'],
                  'status':['exact'], 
                  'order_count':['lt', 'gt']}

class SuppliersFilters(filters.FilterSet):
    status = django_filters.BooleanFilter()
    supplier_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Suppliers
        fields = {'supplier_name': ['exact','icontains'],
                  'status':['exact'], 
                  'order_count':['lt', 'gt']}

class OrderReceivedFilters(filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='exact', method='filter_status')
    user_id__username = django_filters.CharFilter(lookup_expr='icontains')
    buyer_id__buyer_name = django_filters.CharFilter(lookup_expr='icontains')
    item_name= django_filters.CharFilter(lookup_expr='icontains')
    item_cost = django_filters.RangeFilter()
    buyer_id__order_count = django_filters.NumberFilter(lookup_expr='gte')
    date = django_filters.DateFromToRangeFilter()

    def filter_status(self, queryset, name, value):
        return queryset.filter(status=value)
    
    class Meta:
        model = OrdersReceived
        fields = {'user_id__username': ['exact','icontains'],
                  'buyer_id__buyer_name': ['exact','icontains'], 
                  'item_name': ['icontains'],
                  'item_quantity': ['gte'],
                  'item_cost': ['lt','gt'], 
                  'buyer_id__order_count': ['gte'],
                  'date':['exact', 'month__gt'],
                  'status':['exact']

                  }
        
class OrderSentFilters(filters.FilterSet):
    status = django_filters.BooleanFilter()
    user_id__username = django_filters.CharFilter(lookup_expr='icontains')
    supplier_id__supplier_name = django_filters.CharFilter(lookup_expr='icontains')
    item_name = django_filters.CharFilter(lookup_expr='icontains')   
    item_cost = django_filters.RangeFilter()
    supplier_id__order_count = django_filters.NumberFilter(lookup_expr='gte')
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = OrdersSent
        fields = {'user_id__username': ['exact','icontains'],
                  'supplier_id__supplier_name': ['exact','icontains'], 
                  'item_name': ['icontains'],
                  'item_quantity': ['gte'],
                  'item_cost': ['lt','gt'], 
                  'supplier_id__order_count': ['gte'],
                  'date':['exact', 'month__gt'],
                  'status':['exact']

                  }

