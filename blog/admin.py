from django.contrib import admin
from .models import Post


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ['views_count', ]
    search_fields = ['title', 'content']
