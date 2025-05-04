from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Department, Position
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class EmployeeCreationForm(UserCreationForm):
    """Form for creating a new employee with all necessary fields"""
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('username', 'email', 'first_name', 'last_name', 'employee_id', 'position',
                  'gender', 'date_of_birth', 'phone_number', 'address', 'hire_date',
                  'profile_picture', 'is_hr', 'emergency_contact_name', 'emergency_contact_phone')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields required even though they're blank=True in the model
        for field in ['email', 'first_name', 'last_name', 'employee_id', 'gender']:
            self.fields[field].required = True
            
        # Add date widgets with proper formatting
        self.fields['date_of_birth'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'})
        self.fields['hire_date'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'})


class EmployeeUpdateForm(forms.ModelForm):
    """Form for updating an existing employee's information"""
    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'email', 'employee_id', 'position',
                  'gender', 'date_of_birth', 'phone_number', 'address', 'hire_date',
                  'profile_picture', 'is_hr', 'emergency_contact_name', 'emergency_contact_phone')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields required even though they're blank=True in the model
        for field in ['email', 'first_name', 'last_name', 'employee_id', 'gender']:
            self.fields[field].required = True
            
        # Add date widgets with proper formatting
        self.fields['date_of_birth'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'})
        self.fields['hire_date'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'})
        
    def clean_employee_id(self):
        """Validate employee ID is unique (except for the current instance)"""
        employee_id = self.cleaned_data.get('employee_id')
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # Check if any other employee has this ID
            if Employee.objects.exclude(pk=instance.pk).filter(employee_id=employee_id).exists():
                raise ValidationError(_('This employee ID is already in use.'))
        return employee_id


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'