from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, Profile
from . import serializer
from rest_framework.parsers import FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

class UserCreateView(generics.GenericAPIView):
    serializer_class = serializer.UserCreationSerializer
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUsers(generics.GenericAPIView):
    serializer_class = serializer.UserCreationSerializer
    permission_class = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(instance=users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        


class UpdateUserProfile(generics.GenericAPIView):
    serializer_class = serializer.CreateProfileSerializer
    permission_class = [IsAuthenticated]
    parser_classes = [FormParser]
    def put(self, request, user_id):
        file = request.data.get("file")
        print(file)
        prof = get_object_or_404(Profile, user__id=user_id)
        serializer = self.serializer_class(data=file, instance=prof)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
