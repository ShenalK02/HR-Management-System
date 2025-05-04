from django.db import models
from employees.models import Employee

class BirthdayWish(models.Model):
    ANIMATION_CHOICES = [
        ('confetti', 'Confetti'),
        ('balloons', 'Balloons'),
        ('fireworks', 'Fireworks'),
        ('cake', 'Cake Animation'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='birthday_wishes')
    wish_text = models.TextField(help_text="Enter your birthday wish message")
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, 
                                  null=True, related_name='created_wishes')
    created_date = models.DateTimeField(auto_now_add=True)
    animation_type = models.CharField(max_length=50, choices=ANIMATION_CHOICES, default='confetti')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Birthday wish for {self.employee.get_full_name()}"
    
    class Meta:
        verbose_name = "Birthday Wish"
        verbose_name_plural = "Birthday Wishes"
        constraints = [
            models.UniqueConstraint(
                fields=['employee'],
                condition=models.Q(is_active=True),
                name='unique_active_wish_per_employee'
            )
        ]