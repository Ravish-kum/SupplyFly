from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=False)
    company_name = serializers.CharField(required=True, write_only=False)
    phone_number = serializers.CharField(required=True, write_only=False)
    password = serializers.CharField(required=True, write_only=False)
    city = serializers.CharField(required=True, write_only=False)
    address = serializers.CharField(required=True, write_only=False)
    
    class Meta:
        model = User
        fields = ['id','company_name','phone_number',"password",'city','address',
            'is_staff','is_superuser', 'username',  
        ]
        read_only_fields = ['id', 'is_staff', 'is_superuser','phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
    