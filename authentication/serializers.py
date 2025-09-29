from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    class Meta:
        model: CustomUser
        fields = ("id" ,"first_name", "last_name", "email", "password")

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Identifiants invalide")
        
        data['user'] = user
        return data