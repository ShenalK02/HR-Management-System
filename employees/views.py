from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import Employee, Department, Position
from .forms import EmployeeCreationForm, EmployeeUpdateForm, DepartmentForm, PositionForm

# Helper function to check if user is HR
def is_hr(user):
    return user.is_hr

@login_required
def our_team(request):
    employees = Employee.objects.all()
    return render(request, 'employees/our_team.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_list(request):
    """List all employees that the current user has permission to see"""
    if request.user.is_hr:
        # HR can see all employees
        employees = Employee.objects.all().order_by('last_name', 'first_name')
    else:
        # Regular employees can only see themselves
        employees = Employee.objects.filter(pk=request.user.pk)
    
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
@user_passes_test(is_hr)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.username} created successfully!')
            return redirect('employee_list')
        else:
            # Print form errors to debug
            print(f"Form errors: {form.errors}")
    else:
        form = EmployeeCreationForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Create New Employee',
        'can_edit_hr': request.user.is_hr
    })

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    # Check if user has permission to edit this employee
    if not request.user.is_hr and request.user.pk != employee.pk:
        messages.error(request, "You don't have permission to edit this employee.")
        return redirect('employee_list')
    
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, request.FILES, instance=employee)
        
        # Validate form
        if form.is_valid():
            # Regular users can't change HR status
            if not request.user.is_hr:
                form.instance.is_hr = employee.is_hr
                
            # Save the employee
            updated_employee = form.save()
            messages.success(request, f'Employee {updated_employee.get_full_name()} updated successfully!')
            
            # Debug print to confirm save worked
            print(f"Employee updated: {updated_employee.pk}, {updated_employee.get_full_name()}")
            
            # Redirect to detail view
            return redirect('employee_detail', pk=employee.pk)
        else:
            # Print form errors to debug
            print(f"Form errors: {form.errors}")
            messages.error(request, "Error updating employee. Please check the form.")
    else:
        form = EmployeeUpdateForm(instance=employee)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'employee': employee,
        'title': f'Update {employee.get_full_name()}',
        'can_edit_hr': request.user.is_hr
    })

@login_required
@user_passes_test(is_hr)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})

@login_required
@user_passes_test(is_hr)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'employees/department_form.html', {'form': form})

@login_required
@user_passes_test(is_hr)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'employees/department_form.html', {'form': form})
