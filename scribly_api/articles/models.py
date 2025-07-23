from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()
import datetime
from django.utils.timezone import now

def article_image_upload_to(instance, filename):
    today = now().strftime('%Y/%m/%d')
    return f'articles/{today}/{filename}'

class Article(models.Model):
    class ArticleCategory(models.TextChoices):
        sport ='sport'
        programing ='programing'
        politics ='politics'
        economy ='economy'
        technology ='technology'
        health = 'health'
        education = 'education'
        art = 'art'
        culture = 'culture'
        science ='science'
        opinion = 'opinion'
        entertainment ='entertainment'


    title = models.CharField(
        max_length=50,
    )

    text = models.TextField(
        max_length=1000,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    categories = models.CharField(choices=ArticleCategory.choices,default=ArticleCategory.sport)

    is_show = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    image = models.ImageField(upload_to=article_image_upload_to,blank=True,null=True)

    def __str__(self):
        return f'{self.title}'