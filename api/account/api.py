from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime

from rest_registration.utils.responses import get_ok_response
from rest_registration.api.serializers import DefaultUserProfileSerializer

from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,ViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_registration.api.views.base import BaseAPIView 
from rest_framework.request import Request

from .serializers import UserProfileSerializer,\
    VerifyCodeSerializer,User,AuthorizationCode,\
    RegisterUserSerializer,InviteCode,InvitedCodeSerializer,ProfileSerializer

from utils.utils import generate_code, send_code



class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            auth = AuthorizationCode.objects.create(
                user_profile=user,
                code=generate_code()
            )            
            data = auth.code
            res = send_code(data,user.email)
            print(res)
            
            if res:
                user_serializer = UserProfileSerializer(instance=user, context={'request': request})
                return Response({
                    **user_serializer.data,
                })
        
        return Response({"message":"Произощло ошибка"},400)



class VeryfiCodeByEmailAPIView(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'email'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user:
            auth = AuthorizationCode.objects.create(
                user_profile=user,
                code=generate_code()
            )
            
            data = auth.code
            res = send_code(data,user.email)
            if res:
                return get_ok_response(('вам отправлен код'))
            else:
                return Response({"detail": "Failed to send code"}, status=500)
        else:
            return Response({"detail": "User not found"}, status=404)



class ChekingCodeAPI(GenericAPIView):
    queryset = AuthorizationCode.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'code'

    def post(self, request, *args, **kwargs):
        data=self.get_object()
        if data.is_active:
            return get_ok_response("this code is active")
        else:
            return Response({"detail":"this code is not active"},404)



class AuthWithCodeAPIView(GenericAPIView):
    queryset = AuthorizationCode.objects.all()
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'code'

    def get_object(self):
        queryset = self.get_queryset()
        try:
            user = queryset.get(code=self.kwargs['code'])
            return user
        
        except AuthorizationCode.DoesNotExist:
            raise NotFound("Код не подерживается")

    def post(self, request, *args, **kwargs):
        data_t=datetime.today()
        auth_object = self.get_object()
        if auth_object:
            user = auth_object.user_profile
            token = Token.objects.get_or_create(user=user)[0]
            return Response({
            'token': token.key,
            })
        else:
            return Response({"detail":"not defound"},400)    


class ToInviteCodeAPIView(GenericAPIView):
    queryset = InviteCode.objects.all()
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'code'
    serializer_class = InvitedCodeSerializer


    def get_object(self):
        queryset = self.get_queryset()
        try:
            user_code = queryset.get(code=self.kwargs['code'])
            return user_code
        
        except AuthorizationCode.DoesNotExist:
            raise NotFound("Код не суествует")
    
    def get(self, *args, **kwargs):
        user_code_object:InviteCode = self.get_object()
        user:User = self.request.user

        if user_code_object:
            users = user_code_object.users.all()
            if users.exists():
                if not user in users:
                    users.add(user)
                    user_code_object.save()
                else:
                    return Response({"message":"Пользователь уже добавлен"},400)

            data = ProfileSerializer(user_code_object.user_profile).data
        
            return Response({"message":"Пользователь добавлен","data":data})
                
        else:
            return Response({"message":"not defound"},400)



class InviteCodeAPIview(ModelViewSet):
    queryset = InviteCode.objects.all()
    serializer_class = InvitedCodeSerializer