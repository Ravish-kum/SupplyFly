from .models import Suppliers, Buyers, OrdersReceived, OrdersSent
from authentication.models import User
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.views import get_payload_from_token
from rest_framework import status
from .filters import *

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
    
    def get(self, request):
        supplier_data = Suppliers.objects.all()
        supplier_filter = SuppliersFilters(request.GET, queryset=supplier_data)
        supplier_data = supplier_filter.qs

        serializers = SupplierSerializer(supplier_data, many=True)
        if serializers:
            return Response({
                "active suppliers" : serializers.data
            })
        else:
            return Response({"error":"something went wrong"})
    
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
        
    def get(self, request):
        buyer_data = Buyers.objects.all()
        buyer_filter = BuyersFilters(request.GET, queryset=buyer_data)
        buyer_data = buyer_filter.qs

        serializers = BuyerSerializer(buyer_data, many=True)
        
        serializers = BuyerSerializer(buyer_data, many=True)
        if serializers:
            return Response({
                "Buyers" : serializers.data
            })
        else:
            return Response({"error":"something went wrong"})
        
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        # Extract the customer ID from the payload
        if not payload:
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        user_instance = User.objects.filter(id=payload).first()
        if user_instance is None:
            return Response({"error":"something went worng"})
        
        serializer = OrdersReceivedSerializer(data=request.data)

        buyer_name = request.data.get('buyer_name')
        buyer_instance = Buyers.objects.filter(buyer_name=buyer_name).exclude(status=False).first()
        if buyer_instance is None:
            return Response({"error":"buyer does not exist"})
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id = user_instance, buyer_id=buyer_instance)
            buyer_instance.order_count += 1
            buyer_instance.save()
            return Response({'success': 'Order created successfully'})
        
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})
    
    def get(self, request):
        order_received_data = OrdersReceived.objects.all()
        order_received_filter = OrderReceivedFilters(request.GET, queryset=order_received_data)
        order_received_data = order_received_filter.qs

        serializers = OrdersReceivedSerializer(order_received_data, many = True)
        if serializers:
            return Response({
                "suppliers" : serializers.data
            })
        else:
            return Response({"error":"something went wrong"})
        
class OrderSentCreation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        # Extract the customer ID from the payload
        if not payload:
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        user_instance = User.objects.filter(id=payload).first()
        if user_instance is None:
            return Response({"error":"something went worng"})
        
        serializer = OrdersSentSerializer(data=request.data)

        supplier_name = request.data.get('supplier_name')
        supplier_instance = Suppliers.objects.filter(supplier_name=supplier_name).exclude(status=False).first()
        if supplier_instance is None:
            return Response({"error":"supplier does not exist"})
    
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id = user_instance, supplier_id=supplier_instance)
            supplier_instance.order_count += 1
            supplier_instance.save()
            return Response({'success': 'Order created successfully'})
        
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})
        
    def get(self, request):
        export_to_csv_query = None

        order_sent_data = OrdersSent.objects.all()
        params = request.GET
        export_to_csv_query = request.request.query_params.get('export_to_csv')
        order_sent_filter = OrderSentFilters(params, queryset=order_sent_data)
        order_sent_data = order_sent_filter.qs
        if export_to_csv_query is not None:
            pass
        
        print(params)
        serializers = OrdersSentSerializer(order_sent_data, many = True)
        if serializers:
            return Response({
                "suppliers" : serializers.data
            })
        else:
            return Response({"error":"something went wrong"})
        