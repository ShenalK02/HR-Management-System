from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    salary_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_range_max = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.department})"


class Employee(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    employee_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='employee_profiles/', blank=True, null=True)
    is_hr = models.BooleanField(default=False)  # HR flag, default False

    # Group and Permission relationships (custom related_name to avoid clashes)
    groups = models.ManyToManyField(
        Group,
        related_name='employee_groups',  # Unique related_name
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employee_permissions',  # Unique related_name
        blank=True
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')


class PerformanceReview(models.Model):
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Needs Improvement'),
        (3, 'Meets Expectations'),
        (4, 'Exceeds Expectations'),
        (5, 'Outstanding'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='reviews_given')
    date = models.DateField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
    goals = models.TextField(blank=True)

    def __str__(self):
        return f"Performance Review for {self.employee} on {self.date}"
