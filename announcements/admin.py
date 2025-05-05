from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_important', 'expiry_date')
    list_filter = ('is_important', 'created_at', 'expiry_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'