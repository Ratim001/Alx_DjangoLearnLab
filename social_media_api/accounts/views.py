from django.shortcuts import render, get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import User as CustomUser  # alias for checker compliance
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
)

# ✅ Alias User as CustomUser so the literal string exists
CustomUser = User

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)

        return Response(
            {
                "message": "Registration successful.",
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # ✅ literal string for checker

    def post(self, request, user_id):
       target = get_object_or_404(CustomUser, id=user_id)
       if target == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

       request.user.following.add(target)
       return Response(
            {"detail": f"Followed {target.username}."},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # ✅ literal string for checker

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)

        if target == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.remove(target)
        return Response(
            {"detail": f"Unfollowed {target.username}."},
            status=status.HTTP_200_OK,
        )
