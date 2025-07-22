from django.contrib import admin
from .models import Article


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title',  'updated_at','author','is_show')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = [
        ('article info', {
            'fields': ('title','text',)
            }
        ),
        (
        'article info',{
            'fields': ('image','categories','author','is_show')
        }
        )
    ]
    raw_id_fields = ['author']