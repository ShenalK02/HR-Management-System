from django.contrib import admin
from .models import Employee, Department, Position
from .forms import EmployeeCreationForm


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeCreationForm
    list_display = ('username', 'email', 'position', 'is_hr')
    list_filter = ('is_hr', 'position')


admin.site.register(Department)
admin.site.register(Position)

