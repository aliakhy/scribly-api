from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.models import Article
from django.core.paginator import Paginator

User=get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8,max_length=25, write_only=True)

    username=serializers.CharField(
        max_length=25,
        validators=[UniqueValidator(queryset=User.objects.all())],
        error_messages={'unique':'Username already exists'})

    email=serializers.EmailField(
        max_length=50,
        validators=[UniqueValidator(queryset=User.objects.all())],
        error_messages={'unique':'Email already registered'}
        )

    class Meta:
        model = User
        fields=('id','username','email','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user=User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        return user



class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields=('id','title','image')


class ProfileSerializer(serializers.ModelSerializer):
    articles= serializers.SerializerMethodField()

    class Meta:
        model = User
        fields=('id','username','email','about_me','avatar','articles')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
        }

    def get_articles(self,obj):
        request=self.context.get('request')
        page_number=request.query_params.get('page_number',1)
        page_size=6

        queryset=Article.objects.filter(author=obj).order_by('-updated_at')
        paginator=Paginator(queryset,page_size)
        page=paginator.get_page(page_number)

        serializer=ArticleSerializer(page.object_list,many=True,context={'request':request})

        return {
            'count':paginator.count,
            'num_pages':paginator.num_pages,
            'current_page':page.number,
            'results':serializer.data,
        }

    def update(self, instance, validated_data):
        validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True,min_length=8)

