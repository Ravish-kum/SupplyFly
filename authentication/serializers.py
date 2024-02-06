from rest_framework import serializers
from .models import User, CompanyTable



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=False)
    company_name = serializers.SlugRelatedField(slug_field='company_name', queryset=CompanyTable.objects.all())
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
        company_instance  = validated_data['company_name']
        if company_instance:
            company_instance.user_count += 1
            company_instance.save()

        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
    