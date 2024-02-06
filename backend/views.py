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

'''
            SupplierCreation  (class)
It has 2 method POST and GET 
POST : 
    Used to create suppliers by user of a company by these fields ["supplier_name", "contact", "address", "supplier_detail"]
    
    return success response or error in failure
GET :
    Used to fetch all supplier of a company with status True
    
    return list of suppliers
'''
class SupplierCreation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_instance = User.objects.filter(id=payload, company_name__company_name = company_name).first()
        if user_instance is None:
            return Response({"error":"something went worng"})
                
        serializer = SupplierSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id = user_instance)
            return Response({'success': 'supplier created successfully'})
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})
    
    def get(self, request):
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload', "status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        
        supplier_data = Suppliers.objects.filter(user_id__company_name = company_name).exclude(status = False)
        supplier_filter = SuppliersFilters(request.GET, queryset=supplier_data)
        supplier_data = supplier_filter.qs

        serializers = SupplierSerializer(supplier_data, many=True)
        if serializers:
            return Response({
                "active suppliers" : serializers.data  })
        else:
            return Response({"error":"something went wrong"})
    
'''             
                SupplierDeletion (class)
It has 1 method POST
POST :
    Used to delete created Supplier, require supplier_id for deletions
    
    return success response or error in case of failure
'''
class SupplierDeletion(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        supplier_id = request.data.get('supplier_id')
        instance = Suppliers.objects.filter(id = supplier_id).first()
        if instance is not None:
            instance.status = False
            instance.save()
            return Response({"message": "supplier successfully deleted"})
        else:
            return Response({"error":"supplier do not exist by this name" })

'''
            BuyerCreation  (class)
It has 2 method POST and GET 
POST : 
    Used to create Buyers by user of a company by these fields ["Buyer_name", "contact", "address", "Buyer_detail"]
    
    return success response or error in failure
GET :
    Used to fetch all Buyer of a company with status True
    
    return list of Buyers
'''   
class BuyerCreation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        # Extract the customer ID from the payload
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload', "status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_instance = User.objects.filter(id=payload,company_name__company_name = company_name).first()
        if user_instance is None:
            return Response({"error":"something went worng"})
        
        serializer = BuyerSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id = user_instance)
            return Response({'success': 'buyer created successfully'})
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})
        
    def get(self, request):
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        # Extract the customer ID from the payload
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload', "status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        
        buyer_data = Buyers.objects.filter(user_id__company_name = company_name).exclude(status = False)
        buyer_filter = BuyersFilters(request.GET, queryset=buyer_data)
        buyer_data = buyer_filter.qs
        
        serializers = BuyerSerializer(buyer_data, many=True)
        if serializers:
            return Response({
                "Buyers" : serializers.data })
        else:
            return Response({"error":"something went wrong"})
        
'''             
                BuyerDeletion (class)
It has 1 method POST
POST :
    Used to delete created Buyer, require Buyer_id for deletions
    
    return success response or error in case of failure
''' 
class BuyerDeletion(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        buyer_id = request.data.get('buyer_id')
        instance = Buyers.objects.filter(id = buyer_id).first()
        if instance is not None:
            instance.status = False
            instance.save()
            return Response({"message": "Buyer successfully deleted"})
        else:
            return Response({"error":"Buyer do not exist by this name" })

'''     
                OrderReceivedCreation   (class)
It has 2 methods POST and GET 
POST :
    Used to from orders sent by buyers with fields ["buyer_id","buyer_name", "item_name", "item_cost", "item_quantity"]
    
    return success response or error in failure
GET :
    Used to fetch all orders of a company in a list 
'''
class OrderReceivedCreation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))      # payload extaction 
        if error_response:
            return error_response
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload', "status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        user_instance = User.objects.filter(id=payload, company_name__company_name = company_name).first()          # user instance for user foreign key
        if user_instance is None:
            return Response({"error":"something went worng"})
        
        serializer = OrdersReceivedSerializer(data=request.data)

        buyer_id = request.data.get('buyer_id')
        buyer_instance = Buyers.objects.filter(id=buyer_id, user_id__company_name = company_name).exclude(status=False).first() # buyer instance for buyer foreign key
        if buyer_instance is None:
            return Response({"error":"buyer does not exist"})
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id = user_instance, buyer_id=buyer_instance)
            buyer_instance.order_count += 1                     # order count increment for counting total orders came by buyers
            buyer_instance.save()
            return Response({'success': 'Order created successfully'})
        
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})
    
    def get(self, request):
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload', "status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        order_received_data = OrdersReceived.objects.filter(id=payload, company_name__company_name = company_name)
        order_received_filter = OrderReceivedFilters(request.GET, queryset=order_received_data)
        order_received_data = order_received_filter.qs

        serializers = OrdersReceivedSerializer(order_received_data, many = True)
        if serializers:
            return Response({
                "suppliers" : serializers.data
            })
        else:
            return Response({"error":"something went wrong"})

'''     
                OrderSentCreation   (class)
It has 2 methods POST and GET 
POST :
    Used to from orders sent to Suppliers with fields ["supplier_id" ,"supplier_name", "item_name", "item_cost", "item_quantity"]
    
    return success response or error in failure
GET :
    Used to fetch all orders of a company in a list 
'''
class OrderSentCreation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))          # payload extaction 
        if error_response:
            return error_response
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload', "status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        user_instance = User.objects.filter(id=payload,company_name__company_name = company_name).first()               # user instance for user foreign key
        if user_instance is None:
            return Response({"error":"something went worng"})
        
        serializer = OrdersSentSerializer(data=request.data)

        supplier_id = request.data.get('supplier_id')
        supplier_instance = Suppliers.objects.filter(supplier_name=supplier_id, user_id__company_name = company_name).exclude(status=False).first() # buyer instance for supplier foreign key
        if supplier_instance is None:
            return Response({"error":"supplier does not exist"})
    
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id = user_instance, supplier_id=supplier_instance)
            supplier_instance.order_count += 1              # order count increment for counting total orders sent to suppliers
            supplier_instance.save()
            return Response({'success': 'Order created successfully'})
        
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})
        
    def get(self, request):
        
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        # Extract the customer ID from the payload
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload', "status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        order_sent_data = OrdersSent.objects.filter(id=payload,company_name__company_name = company_name)
        order_sent_filter = OrderSentFilters(request.GET, queryset=order_sent_data)
        order_sent_data = order_sent_filter.qs
    
        serializers = OrdersSentSerializer(order_sent_data, many = True)
        if serializers:
            return Response({
                "suppliers" : serializers.data
            })
        else:
            return Response({"error":"something went wrong"})
        