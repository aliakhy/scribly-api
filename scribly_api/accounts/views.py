from tokenize import TokenError
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.permissions import IsAuthenticated ,AllowAny
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginUserView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code ==200:

            username=request.data['username']
            User=get_user_model()
            try:
                user=User.objects.get(username=username)
            except User.DoesNotExist:
                return response
            refresh=response.data['refresh']
            tokens = OutstandingToken.objects.filter(user=user)
            for token in tokens:
                if token.token != refresh:
                    BlacklistedToken.objects.get_or_create(token=token)
            return response


class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response({"message":"this is a protected API"})


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self ):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    def put(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'success':'password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"wrong password"}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        token= request.data.get('refresh')
        if not token:
            return Response({"error":"token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token=RefreshToken(token)
            token.blacklist()
            return Response({'success':'token logged out'}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"detail":f"token is invalid or expire:{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"detail":f"error:{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        email = request.data.get('email')
        try:
            user=get_user_model().objects.get(email=email)
            token=PasswordResetTokenGenerator().make_token(user)
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:8000/accounts/password-reset/confirm/{uidb64}/{token}"
            send_mail(
                subject="Password Reset Request",
                message=f"open the link to change your password :\n{reset_link}",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response({'success':'password reset email sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":f"error:{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=get_user_model().objects.get(pk=uid)


            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error":"token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
            new_password=request.data.get('new_password')

            if not new_password :
                return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

            if len(new_password) < 8:
                return Response({"error": "Password must be at least 8 characters."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'success':'password is changed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":f"error:{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


