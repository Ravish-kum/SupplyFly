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

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token_payload = {'id':user.id}
    access_token = refresh.access_token
    access_token['payload'] = access_token_payload
    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }

def get_payload_from_token(authorization_header):
    secret_key = settings.SECRET_KEY

    if authorization_header is None:
        return None, Response({'error': 'Authorization header missing',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
    
    access_token = authorization_header.split(' ')[1]
   
    try:
        data = jwt.decode(access_token, secret_key, algorithms=['HS256'])['payload']
        payload = data['id']
    except jwt.exceptions.InvalidSignatureError:
        return None, Response({'error': 'Invalid token signature',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.DecodeError:
        return None, Response({'error': 'Invalid token format',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

    return payload, None

class UserSignup(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        phone_number = request.data.get('phone_number')
        phone_number_already_exist = User.objects.filter(phone_number = phone_number).exists()

        if phone_number_already_exist:
            return Response({'error':'User already exists'})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': 'User created successfully'})
        except Exception as e:
            return Response({'error': "not valid",'message':str(e)})

class UserSignin(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            response_tokens_accepter = get_tokens_for_user(user)            
            login(request, user)
        else:
            return Response({'error':"no user or wrong credentials"})
    
        return Response({
                    'message':'signin success',
                    'status_code':200,
                    'refresh_token': response_tokens_accepter['refresh'],
                    'access': response_tokens_accepter['access'] })
    
class UserDetailsUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            return error_response
        # Extract the customer ID from the payload
        if not payload:
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_instance = User.objects.filter(id=payload, is_active=True).first()
        if user_instance is not None:
            updated_user = UserSerializer(user_instance, data=request.data, partial=True)

            if updated_user.is_valid(raise_exception=True):
                updated_user.save()
                return Response({'success':'update done'})
        return Response({"error":"something went wrong"})
