
from django.urls import path
from .views import *

urlpatterns = [
    path("suppliercreation/", SupplierCreation.as_view(), name='suppliercreation'),
    path("supplierdeletion/", SupplierDeletion.as_view(), name='supplierdeletion'),
    path("buyercreation/", BuyerCreation.as_view(), name='buyercreation'),
    path("buyerdeletion/", BuyerDeletion.as_view(), name='buyerdeletion'),

    path("order-received-creation/", OrderReceivedCreation.as_view(), name="order-received-creation"),
    path("order-sent-creation/", OrderSentCreation.as_view(), name="order-sent-creation")
]
