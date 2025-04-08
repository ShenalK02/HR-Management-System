from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employees.models import Employee
from leaves.models import LeaveRequest
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def dashboard(request):
    context = {}

    if request.user.is_hr:
        # HR Dashboard
        total_employees = Employee.objects.count()
        pending_leaves = LeaveRequest.objects.filter(status='P').count()
        context.update({
            'total_employees': total_employees,
            'pending_leaves': pending_leaves,
        })
    else:
        # Employee Dashboard
        my_leaves = LeaveRequest.objects.filter(employee=request.user)
        pending = my_leaves.filter(status='P').count()
        approved = my_leaves.filter(status='A').count()
        rejected = my_leaves.filter(status='R').count()
        context.update({
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
        })

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')