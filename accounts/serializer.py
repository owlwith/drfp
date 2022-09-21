from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import *

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    # def get_cleaned_data(self):
    #     data_dict = super().get_cleaned_data()
    #     data_dict['username'] = self.validated_data.get('username', '')
    #     data_dict['email'] = self.validated_data.get('email', '')
    #     data_dict['password'] = self.validated_data.get('password', '')
    #
    #     return data_dict

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            username = username,
            email = email
        )
        user.set_password(password)
        user.save
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password', None)

        user = authenticate(username = username, password = password)

        if user in None:
            return {'username':'None'}
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                '계정 혹은 비밀번호가 틀렸습니다.'
            )
        return {
            'username':user.username,
            'token':jwt_token
        }

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

