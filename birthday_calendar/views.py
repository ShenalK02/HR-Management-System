from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import BirthdayWish
from .forms import BirthdayWishForm

User = get_user_model()

def is_hr(user):
    return user.groups.filter(name='HR').exists() or user.is_hr

@login_required
@user_passes_test(is_hr)
def calendar_view(request):
    # Get all birthday wishes
    all_wishes = BirthdayWish.objects.all()
    
    # Get all employees with a date of birth
    employees_with_dob = User.objects.exclude(date_of_birth__isnull=True)
    
    # Get today's date
    today = timezone.now().date()
    thirty_days_later = today + timedelta(days=30)
    
    # Process upcoming birthdays (next 30 days)
    upcoming_birthdays = []
    
    for employee in employees_with_dob:
        if employee.date_of_birth:
            # Get this year's birthday
            this_year = today.year
            birth_month = employee.date_of_birth.month
            birth_day = employee.date_of_birth.day
            
            # Create a date for this year's birthday
            this_year_bday = datetime(this_year, birth_month, birth_day).date()
            
            # If birthday has passed this year, use next year's date
            if this_year_bday < today:
                this_year_bday = datetime(this_year + 1, birth_month, birth_day).date()
            
            # Check if within 30 days window
            if today <= this_year_bday <= thirty_days_later:
                # Get wishes for this employee
                wishes = BirthdayWish.objects.filter(employee=employee)
                wish = wishes.first() if wishes.exists() else None
                
                upcoming_birthdays.append({
                    'employee': employee,
                    'birth_date': employee.date_of_birth,
                    'celebration_date': this_year_bday,
                    'days_until': (this_year_bday - today).days,
                    'wish': wish
                })
    
    # Sort by days until birthday
    upcoming_birthdays.sort(key=lambda x: x['days_until'])
    
    # Get today's birthdays
    todays_birthdays = []
    for employee in employees_with_dob:
        if employee.date_of_birth:
            # Check if today is their birthday (ignore year)
            if employee.date_of_birth.month == today.month and employee.date_of_birth.day == today.day:
                # Get wishes for this employee
                wishes = BirthdayWish.objects.filter(employee=employee)
                wish = wishes.first() if wishes.exists() else None
                
                todays_birthdays.append({
                    'employee': employee,
                    'birth_date': employee.date_of_birth,
                    'wish': wish
                })
    
    return render(request, 'birthday_calendar/calendar.html', {
        'all_wishes': all_wishes,
        'upcoming_birthdays': upcoming_birthdays,
        'todays_birthdays': todays_birthdays,
    })

@login_required
@user_passes_test(is_hr)
def create_wish(request, user_id=None):
    employee = None
    if user_id:
        employee = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = BirthdayWishForm(request.POST)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.created_by = request.user
            
            # Set the celebration_date based on the employee's birth date
            if wish.employee and wish.employee.date_of_birth:
                # Get current year
                current_year = timezone.now().year
                month = wish.employee.date_of_birth.month
                day = wish.employee.date_of_birth.day
                
                # Set the celebration date to this year's birthday
                wish.celebration_date = datetime(current_year, month, day).date()
                
                # If birthday has already passed this year, set for next year
                if wish.celebration_date < timezone.now().date():
                    wish.celebration_date = datetime(current_year + 1, month, day).date()
            
            wish.save()
            messages.success(request, 'Birthday wish created successfully!')
            return redirect('birthday_calendar:calendar')
    else:
        initial_data = {}
        if employee:
            initial_data['employee'] = employee
        form = BirthdayWishForm(initial=initial_data)
    
    return render(request, 'birthday_calendar/create_wish.html', {
        'form': form,
        'employee': employee
    })

@login_required
def view_wish(request, wish_id):
    wish = get_object_or_404(BirthdayWish, id=wish_id)
    today = timezone.now().date()
    
    # Check if it's the person's birthday today
    is_birthday_today = False
    if wish.employee.date_of_birth:
        is_birthday_today = (wish.employee.date_of_birth.month == today.month and 
                            wish.employee.date_of_birth.day == today.day)
    
    # Get all wishes for this user to show multiple messages
    all_user_wishes = BirthdayWish.objects.filter(employee=wish.employee)
    
    return render(request, 'birthday_calendar/view_wish.html', {
        'wish': wish,
        'is_birthday_today': is_birthday_today,
        'all_user_wishes': all_user_wishes,
    })

@login_required
@user_passes_test(is_hr)
def edit_wish(request, wish_id):
    wish = get_object_or_404(BirthdayWish, id=wish_id)
    
    if request.method == 'POST':
        form = BirthdayWishForm(request.POST, instance=wish)
        if form.is_valid():
            updated_wish = form.save(commit=False)
            
            # Update the celebration_date based on the employee's birth date if employee changed
            if updated_wish.employee and updated_wish.employee.date_of_birth:
                current_year = timezone.now().year
                month = updated_wish.employee.date_of_birth.month
                day = updated_wish.employee.date_of_birth.day
                
                # Set the celebration date to this year's birthday
                updated_wish.celebration_date = datetime(current_year, month, day).date()
                
                # If birthday has already passed this year, set for next year
                if updated_wish.celebration_date < timezone.now().date():
                    updated_wish.celebration_date = datetime(current_year + 1, month, day).date()
            
            updated_wish.save()
            messages.success(request, 'Birthday wish updated successfully!')
            return redirect('birthday_calendar:view_wish', wish_id=wish.id)
    else:
        form = BirthdayWishForm(instance=wish)
    
    return render(request, 'birthday_calendar/create_wish.html', {
        'form': form,
        'editing': True,
        'wish': wish
    })

@login_required
@user_passes_test(is_hr)
def delete_wish(request, wish_id):
    wish = get_object_or_404(BirthdayWish, id=wish_id)
    
    if request.method == 'POST':
        wish.delete()
        messages.success(request, 'Birthday wish deleted successfully!')
        return redirect('birthday_calendar:calendar')
    
    return render(request, 'birthday_calendar/delete_confirmation.html', {
        'wish': wish
    })

@login_required
def todays_birthdays(request):
    """Function to get today's birthdays for the dashboard"""
    today = timezone.now().date()
    
    # Find employees whose birthdays are today
    birthday_employees = User.objects.exclude(date_of_birth__isnull=True).filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )
    
    # Get wishes for those employees that should be displayed on dashboard
    birthday_wishes = BirthdayWish.objects.filter(
        employee__in=birthday_employees,
        display_on_dashboard=True
    )
    
    return render(request, 'birthday_calendar/dashboard_birthdays.html', {
        'birthday_wishes': birthday_wishes,
        'birthday_employees': birthday_employees,
    })