from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Employee, Department
from .forms import EmployeeCreationForm, EmployeeUpdateForm, DepartmentForm

def is_hr(user):
    return user.is_authenticated and user.is_hr

@login_required
def employee_list(request):
    if request.user.is_hr:
        employees = Employee.objects.all()
    else:
        employees = Employee.objects.filter(is_hr=False)
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreationForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

@user_passes_test(is_hr)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})

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
@user_passes_test(lambda u: u.is_hr)  # Only HR can create employees
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.username} created successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Create New Employee'
    })


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    # Only HR can update HR status
    can_edit_hr = request.user.is_hr

    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            if not request.user.is_hr:
                # Preserve original HR status if non-HR is editing
                form.instance.is_hr = employee.is_hr
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeUpdateForm(instance=employee)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'employee': employee,
        'can_edit_hr': can_edit_hr,
        'title': f'Update {employee.username}'
    })

