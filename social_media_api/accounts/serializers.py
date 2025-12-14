from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "bio", "profile_picture"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        # ✅ Use create_user
        user = User.objects.create_user(password=password, **validated_data)
        # ✅ Use Token.objects.create
        Token.objects.create(user=user)
        return user
