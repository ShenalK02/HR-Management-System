from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ReviewSchedule, ReviewFeedback

class ReviewFeedbackInline(admin.StackedInline):
    model = ReviewFeedback
    extra = 0

@admin.register(ReviewSchedule)
class ReviewScheduleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'scheduled_date', 'status')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__email')
    inlines = [ReviewFeedbackInline]

@admin.register(ReviewFeedback)
class ReviewFeedbackAdmin(admin.ModelAdmin):
    list_display = ('review', 'final_rating', 'is_published', 'published_date')
    list_filter = ('is_published', 'final_rating')