from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Article
from .serializers import  ArticleSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from .permissions import ArticlePermissions


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_show=True).order_by('-updated_at')
    serializer_class = ArticleSerializer
    permission_classes = [ArticlePermissions]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




