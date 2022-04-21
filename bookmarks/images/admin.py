from django.contrib import admin

# Register your models here.
from images.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'likes', 'sort_desc', 'image', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'image')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
