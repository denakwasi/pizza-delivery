from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import User, Profile
from rest_framework.decorators import action
from . import serializer
from .serializer import CreateProfileSerializer, UserCreationSerializer
from rest_framework.parsers import JSONParser, FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

class UserCreateView(generics.GenericAPIView):
    serializer_class = serializer.UserCreationSerializer
    # parser_classes = (MultiPartParser, FormParser,)
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data) # self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 


class AllUsers(generics.GenericAPIView):
    serializer_class = serializer.UserCreationSerializer
    permission_class = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(instance=users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        

class UpdateUser(generics.GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializer.UserCreationSerializer
    # parser_classes = [MultiPartParser, FormParser]

    def put(self, request, user_id):
        data = request.data
        user = get_object_or_404(User, pk=user_id)
        serializer = self.serializer_class(data=data, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteUser(generics.GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = serializer.UserCreationSerializer

    def delete(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        if user:
            if not user.is_superuser:
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateUserProfile(generics.GenericAPIView):
    serializer_class = serializer.CreateProfileSerializer
    # permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    
    def put(self, request, img_id):
        data = request.FILES
        print(request.data)
        prof = get_object_or_404(Profile, pk=img_id)
        serializer = self.serializer_class(data=data, instance=prof)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # d

