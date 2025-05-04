from django.contrib import admin
from .models import BirthdayWish

@admin.register(BirthdayWish)
class BirthdayWishAdmin(admin.ModelAdmin):
    list_display = ['employee', 'celebration_date', 'celebration_style', 'created_by']
    list_filter = ['celebration_date', 'celebration_style']
    search_fields = ['employee__username', 'message', 'description']
    date_hierarchy = 'celebration_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('employee', 'created_by')
        }),
        ('Birthday Details', {
            'fields': ('celebration_date', 'celebration_style', 'message', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )