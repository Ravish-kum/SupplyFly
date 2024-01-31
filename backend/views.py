from .models import Suppliers, Buyers, OrdersReceived, OrdersSent
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class SupplierCreation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def post(self,request):
        serializer = SupplierSerializer(data=request.data)
        supplier_name = request.data.get('supplier_name')
        supplier_already_exist = Suppliers.objects.filter(supplier_name = supplier_name).exists()

        if supplier_already_exist:
            return Response({'error':'supplier already exists'})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': 'supplier created successfully'})
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})
    
class SupplierDeletion(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        name_of_supplier = request.data.get('supplier_name')
        instance = Suppliers.objects.filter(supplier_name = name_of_supplier).first()
        if instance is not None:
            instance.status = False
            instance.save()
            return Response({"message": "supplier successfully deleted"})
        else:
            return Response({"error":"supplier do not exist by this name" })
        
class BuyerCreation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self,request):
        serializer = BuyerSerializer(data=request.data)
        buyer_name = request.data.get('buyer_name')
        buyer_already_exist = Buyers.objects.filter(buyer_name = buyer_name).exists()

        if buyer_already_exist:
            return Response({'error':'buyer already exists'})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': 'buyer created successfully'})
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})
    
class BuyerDeletion(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name_of_buyer = request.data.get('buyer_name')
        instance = Buyers.objects.filter(buyer_name = name_of_buyer).first()
        if instance is not None:
            instance.status = False
            instance.save()
            return Response({"message": "Buyer successfully deleted"})
        else:
            return Response({"error":"Buyer do not exist by this name" })
        
    
class OrderReceivedCreation(APIView):

    def post(self,request):
        serializer = OrdersReceivedSerializer(data=request.data)
        buyer_name = request.data.get('buyer_name')
        buyer_already_exist = Buyers.objects.filter(buyer_name = buyer_name).exists()

        if buyer_already_exist:
            return Response({'error':'buyer already exists'})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': 'buyer created successfully'})
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})