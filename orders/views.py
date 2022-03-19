from ast import Or
from django.http import request
from django.shortcuts import render, get_object_or_404
from .models import Order
from rest_framework import generics, status
from rest_framework.response import Response
# from .models import User
from . import serializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth import get_user_model
User = get_user_model()


class HelloAuthView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message": "Hello world"}, status=status.HTTP_200_OK)



class  OrderCreateListView(generics.GenericAPIView):
    serializer_class = serializer.OrderCreationSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        user = request.user
        
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class OrderDetailView(generics.GenericAPIView):
    serializer_class = serializer.OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        data = request.data
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(data=data, instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class = serializer.OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        data = request.data
        serializer = self.serializer_class(data=data, instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(generics.GenericAPIView):
    serializer_class = serializer.OrderDetailSerializer

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            orders = Order.objects.all().filter(customer=user)
            serializer = self.serializer_class(instance=orders, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserOrderDetail(generics.GenericAPIView):
    serializer_class = serializer.OrderDetailSerializer

    def get(self, request, user_id, order_id):
        user = User.objects.get(pk=user_id)
        order = Order.objects.all().filter(customer=user).filter(pk=order_id)
        serializer = self.serializer_class(instance=order, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DeleteAllUserOrders(generics.GenericAPIView):
    def delete(self, request, user_id):
        orders = Order.objects.all().filter(customer_id=user_id)
        for order in orders:
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
