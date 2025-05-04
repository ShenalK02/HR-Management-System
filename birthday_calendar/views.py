from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.functions import Extract
from django.db.models import F, ExpressionWrapper, DateField, Case, When, Value

from employees.models import Employee
from .models import BirthdayWish

@login_required
def birthday_calendar(request):
    """Main calendar view showing all employee birthdays"""
    employees = Employee.objects.all().order_by(
        Extract('date_of_birth', 'month'),
        Extract('date_of_birth', 'day')
    )
    
    # Check if user is HR to enable special features
    is_hr = request.user.is_hr
    
    context = {
        'employees': employees,
        'is_hr': is_hr,
    }
    return render(request, 'birthday_calendar/calendar.html', context)

@login_required
def create_birthday_wish(request, employee_id):
    """Create a birthday wish for an employee (HR only)"""
    # Check if user is HR
    if not request.user.is_hr:
        return redirect('birthday_calendar:calendar')
    
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        wish_text = request.POST.get('wish_text')
        description = request.POST.get('description')
        animation_type = request.POST.get('animation_type')
        
        # Deactivate any existing active wishes for this employee
        BirthdayWish.objects.filter(employee=employee, is_active=True).update(is_active=False)
        
        # Create new wish
        BirthdayWish.objects.create(
            employee=employee,
            wish_text=wish_text,
            description=description,
            created_by=request.user,
            animation_type=animation_type
        )
        return redirect('birthday_calendar:calendar')
    
    context = {
        'employee': employee,
    }
    return render(request, 'birthday_calendar/create_wish.html', context)

@login_required
def view_birthday_wish(request, wish_id):
    """View a specific birthday wish"""
    wish = get_object_or_404(BirthdayWish, id=wish_id, is_active=True)
    
    context = {
        'wish': wish,
    }
    return render(request, 'birthday_calendar/view_wish.html', context)

@login_required
def upcoming_birthdays_api(request):
    """API endpoint to get upcoming birthdays in the next 30 days"""
    today = timezone.now().date()
    thirty_days_later = today + timedelta(days=30)
    
    # Create a calculated field for this year's birthday
    employees = Employee.objects.annotate(
        birthday_month=Extract('date_of_birth', 'month'),
        birthday_day=Extract('date_of_birth', 'day'),
        next_birthday=ExpressionWrapper(
            Case(
                # If birthday already passed this year, use next year's date
                When(
                    birthday_month__lt=today.month,
                    then=Value(f"{today.year + 1}-") + F('birthday_month') + Value(f"-{F('birthday_day')}")
                ),
                When(
                    birthday_month=today.month,
                    birthday_day__lt=today.day,
                    then=Value(f"{today.year + 1}-") + F('birthday_month') + Value(f"-{F('birthday_day')}")
                ),
                # Otherwise use this year's date
                default=Value(f"{today.year}-") + F('birthday_month') + Value(f"-{F('birthday_day')}")
            ),
            output_field=DateField()
        )
    ).filter(
        next_birthday__lte=thirty_days_later,
        next_birthday__gte=today
    ).order_by('next_birthday')
    
    birthdays = []
    for employee in employees:
        # Check if employee has an active birthday wish
        wish = BirthdayWish.objects.filter(employee=employee, is_active=True).first()
        
        birthdays.append({
            'id': employee.id,
            'name': employee.get_full_name(),
            'next_birthday': employee.next_birthday.strftime('%Y-%m-%d'),
            'has_wish': wish is not None,
            'wish_id': wish.id if wish else None
        })
    
    return JsonResponse({'birthdays': birthdays})