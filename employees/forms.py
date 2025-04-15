from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee, Department, Position


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('username', 'email', 'first_name', 'last_name', 'employee_id', 'position',
                  'gender', 'date_of_birth', 'phone_number', 'address', 'profile_picture', 'is_hr')

class EmployeeUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'email', 'employee_id', 'position',
                  'gender', 'date_of_birth', 'phone_number', 'address',
                  'profile_picture', 'is_hr', 'emergency_contact_name', 'emergency_contact_phone')


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'