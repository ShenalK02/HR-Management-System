from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employees.models import Employee
from leaves.models import LeaveRequest
from django.contrib.auth import logout
from django.shortcuts import redirect
from performance_reviews.models import ReviewSchedule
from django.utils import timezone
from django.db.models import Q
from announcements.models import Announcement

@login_required
def dashboard(request):
    context = {}
    
    # Get recent and active announcements
    today = timezone.now().date()
    recent_announcements = Announcement.objects.filter(
        Q(expiry_date__gte=today) | Q(expiry_date__isnull=True)
    ).order_by('-is_important', '-created_at')[:3]
    
    # Add announcements to context
    context['recent_announcements'] = recent_announcements
    
    if request.user.is_hr:
        # HR Dashboard
        total_employees = Employee.objects.count()
        pending_leaves = LeaveRequest.objects.filter(status='P').count()
        
        # Add upcoming reviews
        upcoming_reviews = ReviewSchedule.objects.filter(
            scheduled_date__gte=timezone.now()
        ).order_by('scheduled_date')[:5]  # Show next 5 upcoming reviews
        
        context.update({
            'total_employees': total_employees,
            'pending_leaves': pending_leaves,
            'upcoming_reviews': upcoming_reviews,
        })
    else:
        # Employee Dashboard
        my_leaves = LeaveRequest.objects.filter(employee=request.user)
        pending = my_leaves.filter(status='P').count()
        approved = my_leaves.filter(status='A').count()
        rejected = my_leaves.filter(status='R').count()
        
        # Add upcoming reviews for the employee
        my_upcoming_reviews = ReviewSchedule.objects.filter(
            employee=request.user,
            scheduled_date__gte=timezone.now()
        ).order_by('scheduled_date')[:3]  # Show next 3 upcoming reviews
        
        context.update({
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'my_upcoming_reviews': my_upcoming_reviews,
        })
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')