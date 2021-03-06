from django.contrib import admin
from .models import Media

class MediaAdmin(admin.ModelAdmin):
    list_filter = ("user", "media_type", "custom_identifier")
    list_display = ("identifier", "user", "media_type", "custom_identifier", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("custom_identifier", "hash", "media_type", "created_at")

admin.site.register(Media, MediaAdmin)