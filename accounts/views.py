from django.shortcuts import render
from rest_framework import serializers, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotAuthenticated, NotFound
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from accounts.serializers import UserSerializer


class RegistrationView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'mgs': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @csrf_exempt
    def post(self, request):
        data = request.data           
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user  = User.objects.get(username=data['username'])
            token = Token.objects.get(user=user)
            
            return Response(
                {
                    'message': 'User is created successfully',
                    'user'   : serializer.data,
                    'token'  : token.key,
                    
                },
                status=status.HTTP_201_CREATED
            )
        else:
            msg_res = serializer.errors
            return Response(msg_res, status=status.HTTP_400_BAD_REQUEST)
            
    @csrf_exempt
    def put(self, request, id=None):
        if id:
            data = request.data
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=data) # all fields
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                msg = {'msg': 'Data complete update successfully'}
                return Response(msg, serializer.data, status=status.HTTP_200_OK)
            else:
                msg = serializer.errors
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            msg = {'error': 'Id not found'}
            return Response(msg, status=status.HTTP_501_NOT_IMPLEMENTED)
        
    @csrf_exempt
    def patch(self, request, id=None):
        if id:
            data = request.data
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=data, partial=True) # not required all fileds
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                msg = {'msg': 'Data partial update successfully'}
                return Response(msg, serializer.data, status=status.HTTP_200_OK)
            else:
                msg = serializer.errors
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            msg = {'error': 'Id not found'}
            return Response(msg, status=status.HTTP_501_NOT_IMPLEMENTED)
        
            
    @csrf_exempt
    def delete(self, request, id=None):
        if id:
            user = User.objects.get(id=id)
            if user:
                user.delete()
                msg = {'message': 'User is deleted successfully'}
                return Response(msg, status=status.HTTP_200_OK)
            else:
                msg = {'error': 'User is not found'}
                return Response(msg, status=status.HTTP_404_NOT_FOUND)
        else:
            msg = {'error': 'Id not found'}
            return Response(msg, status=status.HTTP_501_NOT_IMPLEMENTED)


class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        print(username, 'line 108')
        if not username:
            return Response({'error': 'Username should not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Password should not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            e_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Username not found'}, status=status.HTTP_404_NOT_FOUND)
               
        if not e_user.check_password(password):
            return Response({'error': 'Password not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        auth_user = authenticate(username=username, password=password)
        
        if auth_user is not None:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            msg = {
                'message': 'User login successfull',
                'data'   : serializer.data,
            }
            token, create = Token.objects.get_or_create(user=user)
            msg['token'] = token.key
            
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg = {'error': 'Auth user is none'}
            return Response(msg, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes=[IsAuthenticated,]
    @csrf_exempt
    def post(self,request):
        token=Token.objects.get(user=request.user)
        if token:
            token.delete()
            msg = {
                'message': 'User logout successfully',
                'redirect': 'http://127.0.0.1:8000/login/',
                
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg = {'error': 'Token not found'}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)


