from django.contrib.auth.views import PasswordResetView

app_name = 'accounts'
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/',ProtectedAPIView.as_view(), name='protected'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', RequestPasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
]