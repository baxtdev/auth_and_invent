from random import randint
from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField
from account.models import InviteCode, User,AuthorizationCode


class RegisterUserSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=False)
    email = serializers.EmailField(required=False)
    class Meta:
        fields = (
            'phone',
            'email',
        )

    def create(self, validated_data):
        phone = validated_data.pop('phone',None)
        email = validated_data.pop('email',None)
        
        if phone:
            user,_ = User.objects.get_or_create(phone=phone)
        
        else :
            user,_ = User.objects.get_or_create(email=email)

        if phone:
            user.phone=phone
            
        if email:
            user.email=email    
        user.save()
        return user  
    


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
    class Meta:
        fields = ['code']
   





class ProfileSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(source='invited_code.code',read_only=True)
    class Meta:
        model = User
        fields = (
            'id', 
            'email',
            'first_name',
            'last_name',
            'phone',
            'get_full_name',
            'invite_code'
            )
        read_only_fields = ('email',) 


class InvitedCodeSerializer(serializers.ModelSerializer):
    users = ProfileSerializer(read_only=True,many=True)

    class Meta:
        model = InviteCode
        fields = (
            'code',
            'users',
            'count_invited_users',
            )    


class UserProfileSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(source='invited_code.code',read_only=True)
    invited_users = ProfileSerializer(many=True,source='invited_code.users',read_only=True)
    class Meta:
        model = User
        fields = (
            'id', 
            'email',
            'first_name',
            'last_name',
            'phone',
            'get_full_name',
            'invite_code',
            'invited_users'
            )
