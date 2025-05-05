from django.db import models
from django.conf import settings
from django.utils import timezone

class BirthdayWish(models.Model):
    # Update User references to use settings.AUTH_USER_MODEL
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='birthday_wishes')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_wishes')
    message = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # This will be populated from the employee's date_of_birth
    celebration_date = models.DateField(default=timezone.now)
    
    # Choose from a set of celebration styles
    CELEBRATION_STYLES = [
        ('confetti', 'Confetti'),
        ('balloons', 'Balloons'),
        ('fireworks', 'Fireworks'),
        ('cake', 'Cake Animation'),
        ('stars', 'Stars'),
    ]
    celebration_style = models.CharField(max_length=20, choices=CELEBRATION_STYLES, default='confetti')
    
    # Flag to indicate if this wish should be displayed on the main dashboard
    display_on_dashboard = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Birthday wish for {self.employee.username} on {self.celebration_date}"
    
    class Meta:
        ordering = ['celebration_date']