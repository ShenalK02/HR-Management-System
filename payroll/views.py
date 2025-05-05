from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payroll
from .forms import PayrollForm

@login_required
def add_payroll(request):
    # Ensure only HR can access this view
    if not request.user.is_hr:
        return redirect('dashboard')

    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_dashboard')
    else:
        form = PayrollForm()

    return render(request, 'payroll/add_payroll.html', {'form': form})


@login_required
def payroll_dashboard(request):
    payrolls = Payroll.objects.all().order_by('-payment_date')
    return render(request, 'payroll/payroll_dashboard.html', {'payrolls': payrolls})
