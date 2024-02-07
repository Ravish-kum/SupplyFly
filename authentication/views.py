from rest_framework.views import APIView
from authentication.serializers import UserSerializer
from authentication.models import User
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, login
User = get_user_model()
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

'''         get_token_for_user (function)
Used for formation of Refresh and Access token by JWT       '''

def get_tokens_for_user(user):
    if not user:
        return Response({"error":"user instance not found"},status= status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    # extracting company_name from CompanyTable through foreign key in User table (user.company_name.company_name)
    access_token_payload = {'id':user.id, 'company_name':user.company_name.company_name}
    access_token = refresh.access_token
    access_token['payload'] = access_token_payload
    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }

'''         
            get_payload_form_token (function)
Used for fetching paload (user id , error (if any) and company name)       
'''
def get_payload_from_token(authorization_header):
    secret_key = settings.SECRET_KEY

    if authorization_header is None:
        return None, Response({'error': 'Authorization header missing',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
    access_token = authorization_header.split(' ')[1]
   
    try:
        data = jwt.decode(access_token, secret_key, algorithms=['HS256'])['payload']
        payload, company_name = data['id'], data['company_name']
    except jwt.exceptions.InvalidSignatureError:
        return None, Response({'error': 'Invalid token signature',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.DecodeError:
        return None, Response({'error': 'Invalid token format',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
                
    return payload, None, company_name  

'''         
                UserSignup (class)
It has 1 method post
POST  :
    Used for formation of new user using nessary fields [ "username", "phone_number", "password", "city", "address", "company_name"] 
    where company_name is a foreign key of CompanyTable 
    
    return success response if created new user or error in case of failure
'''
class UserSignup(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        phone_number = request.data.get('phone_number')
        phone_number_already_exist = User.objects.filter(phone_number = phone_number).exists()

        if phone_number_already_exist:
            return Response({'error':'User already exists',"status_code":409}, status=status.HTTP_409_CONFLICT)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'User created successfully',"status_code":201}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': "not valid",'message':str(e),"status_code":500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
                UserSignin (class)
It has 1 method post 
POST :
    Used for user login using JWT, it takes [phone_number, password] of the user to authenticate
    
    return success response with refresh_token, access or error in case of failure
'''
class UserSignin(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            response_tokens_accepter = get_tokens_for_user(user)            
            login(request, user)
        else:
            return Response({'error':"no user or wrong credentials","status_code":400}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({
                    'message':'signin success',
                    'refresh_token': response_tokens_accepter['refresh'],
                    'access': response_tokens_accepter['access'] ,
                    "status_code":200}, status=status.HTTP_200_OK)
    
'''
            UserDetailUpdate (class)
It has 1 method put 
PUT :
    Used for updating details of the user, required to be logined for updating details

    return success response or error in case of failure
'''
class UserDetailsUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        payload, error_response, company_name = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        if not payload or not company_name:
            return Response({'error': 'Customer ID or Company name not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        user_instance = User.objects.filter(id=payload, is_active=True, company_name__company_name = company_name).first()
        if user_instance is not None:
            updated_user = UserSerializer(user_instance, data=request.data, partial=True)

            if updated_user.is_valid(raise_exception=True):
                updated_user.save()
                return Response({'message':'update done to user', "status_code":200}, status=status.HTTP_200_OK)
        return Response({"error":"something went wrong","status_code":500},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
