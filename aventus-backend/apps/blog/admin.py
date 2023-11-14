from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date','is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description',)

admin.site.register(Blog, BlogAdmin)
