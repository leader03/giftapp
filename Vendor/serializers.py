from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *


class CustomerRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(required=True)
    phone_number = serializers.IntegerField(required=True)
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'password2', 'name', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        customer = CustomerUser.objects.create(
            user=user,
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            username = validated_data['username'],
            email=validated_data['email'],
        )
        customer.save()
        return customer
        

class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user is not None and CustomerUser.objects.filter(user=user).exists():
            token = super(CustomerTokenObtainPairSerializer, cls).get_token(user)
            token['username'] = user.username
            return token
        elif user is not None and VendorUser.objects.filter(user=user).exists():
            token = super(CustomerTokenObtainPairSerializer, cls).get_token(user)
            token['username'] = user.username
            return token
        else:
            return None



class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'

class VendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorUser
        fields = '__all__'

class QrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qr
        fields = '__all__'