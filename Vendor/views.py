from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .models import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import filters
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated


class CustomerTokenObtainPairView(TokenObtainPairView):
    permissions_classes = (AllowAny,)
    serializer_class = CustomerTokenObtainPairSerializer 

class CustomerRegisterView(generics.CreateAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerRegisterSerializer

class EditCustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        customer = CustomerUser.objects.get(user=request.user)
        serializer = CustomerUserSerializer(customer, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        customer = CustomerUser.objects.get(user=request.user)
        data = {
            'user': customer.user.id,
            'name': request.data.get('name'),
            'phone_number': request.data.get('phone_number'),
            'username': request.data.get('username'),
            'email':request.data.get('email'),
            'address': request.data.get('address'),
        }
        serializer = CustomerUserSerializer(customer,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QrView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = {
            'qrscanned': True
        }
        serializer = QrSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAuthView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if CustomerUser.objects.filter(user=request.user).exists():
                customer = CustomerUser.objects.get(user=request.user)
                serializer = CustomerUserSerializer(customer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif VendorUser.objects.filter(user=request.user).exists():
                vendor = VendorUser.objects.get(user=request.user)
                serializer = VendorUserSerializer(vendor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
