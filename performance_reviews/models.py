from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from employees.models import Employee
from django.utils import timezone

class ReviewSchedule(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews')
    scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scheduled_reviews')
    department_head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dept_head_reviews')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    
    def __str__(self):
        return f"Review for {self.employee} on {self.scheduled_date.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-scheduled_date']

class ReviewFeedback(models.Model):
    review = models.OneToOneField(ReviewSchedule, on_delete=models.CASCADE, related_name='feedback')
    employee_feedback = models.TextField(blank=True)
    department_head_feedback = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    final_rating = models.PositiveSmallIntegerField(default=0, help_text="Rating from 1-5")
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Feedback for {self.review}"
