app_name = 'articles'
from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'', ArticleViewSet)
urlpatterns = [
    path('',include(router.urls)),
]