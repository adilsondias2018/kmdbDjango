from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import LoginSerializer, UserSerializer


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        if User.objects.filter(username=serializer.validated_data['username']).exists():

            return Response({'username': ['A user with that username already exists.']}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**serializer.validated_data)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(**serializer.validated_data)

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        else:
            return Response({'Unauthorized':'Faile to authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

