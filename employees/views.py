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
    employees = Employee.objects.all()
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

# Similar views for Position CRUD operations