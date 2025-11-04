from django.rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        data['user'] = user
        return data
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta :
        model = CustomUser
        fields = ('id','username','first_name', 'last_name', 'email', 'password')

    def validate(self, profile_data):
        if not profile_data:
            raise serializers.ValidationError({ f"Missing data"})

        profile_data['profile_data'] = profile_data
        return profile_data

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile_data= validated_data.pop('profile_data')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    