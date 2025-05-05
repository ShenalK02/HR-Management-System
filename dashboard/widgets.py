from django.utils import timezone
from django.contrib.auth import get_user_model
from birthday_calendar.models import BirthdayWish

User = get_user_model()

def get_upcoming_birthdays_widget(request):
    """
    Get today's birthdays and upcoming birthdays for the dashboard widget
    """
    today = timezone.now().date()
    
    # Find employees whose birthdays are today
    todays_birthday_employees = User.objects.exclude(date_of_birth__isnull=True).filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )
    
    # Get wishes for those employees that should be displayed on dashboard
    todays_birthday_wishes = BirthdayWish.objects.filter(
        employee__in=todays_birthday_employees,
        display_on_dashboard=True
    )
    
    # Group wishes by employee for easier template rendering
    todays_celebrations = []
    for employee in todays_birthday_employees:
        wishes = todays_birthday_wishes.filter(employee=employee)
        wish = wishes.first() if wishes.exists() else None
        
        todays_celebrations.append({
            'employee': employee,
            'wish': wish,
        })
    
    # Get upcoming birthdays (next 30 days, excluding today)
    thirty_days_later = today + timezone.timedelta(days=30)
    upcoming_birthdays = []
    
    employees_with_dob = User.objects.exclude(date_of_birth__isnull=True)
    
    for employee in employees_with_dob:
        if employee.date_of_birth:
            # Get this year's birthday
            this_year = today.year
            birth_month = employee.date_of_birth.month
            birth_day = employee.date_of_birth.day
            
            # Create a date for this year's birthday
            this_year_bday = timezone.datetime(this_year, birth_month, birth_day).date()
            
            # If birthday has passed this year, use next year's date
            if this_year_bday < today:
                this_year_bday = timezone.datetime(this_year + 1, birth_month, birth_day).date()
            
            # Check if within 30 days window but not today
            if today < this_year_bday <= thirty_days_later:
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
    
    return {
        'todays_celebrations': todays_celebrations,
        'upcoming_birthdays': upcoming_birthdays[:5]  # Limit to 5 upcoming birthdays
    }
