from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import ReviewSchedule, ReviewFeedback
from .forms import ReviewScheduleForm, ReviewFeedbackForm
from django.utils import timezone

@login_required
def review_calendar(request):
    """View for displaying upcoming reviews based on user role"""
    if request.user.is_hr:  # This is fine - your model has is_hr field
        # HR can see all scheduled reviews
        upcoming_reviews = ReviewSchedule.objects.filter(
            scheduled_date__gte=timezone.now()
        ).order_by('scheduled_date')
    elif hasattr(request.user, 'is_department_head') and request.user.is_department_head:
        # Department heads see reviews for their department members
        upcoming_reviews = ReviewSchedule.objects.filter(
            department_head=request.user,
            scheduled_date__gte=timezone.now()
        ).order_by('scheduled_date')
    else:
        # Regular employees see only their reviews
        upcoming_reviews = ReviewSchedule.objects.filter(
            employee=request.user,  # Changed from employee__user=request.user
            scheduled_date__gte=timezone.now()
        ).order_by('scheduled_date')
    
    past_reviews = ReviewSchedule.objects.filter(
        scheduled_date__lt=timezone.now()
    ).order_by('-scheduled_date')
    
    return render(request, 'performance_reviews/calendar.html', {
        'upcoming_reviews': upcoming_reviews,
        'past_reviews': past_reviews
    })

@login_required
def schedule_review(request):
    """View for HR to schedule a new review"""
    if not request.user.is_hr:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    if request.method == 'POST':
        form = ReviewScheduleForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.scheduled_by = request.user
            review.save()
            messages.success(request, 'Performance review scheduled successfully!')
            return redirect('review_calendar')
    else:
        form = ReviewScheduleForm()
    
    return render(request, 'performance_reviews/schedule_review.html', {'form': form})

@login_required
def review_detail(request, pk):
    """View details of a specific review"""
    review = get_object_or_404(ReviewSchedule, pk=pk)
    
    # Check permissions
    if not (request.user.is_hr or 
            request.user == review.department_head or 
            request.user == review.employee):  # Changed from review.employee.user
        return HttpResponseForbidden("You don't have permission to view this review.")
    
    # Get or create feedback object
    feedback, created = ReviewFeedback.objects.get_or_create(review=review)
    
    return render(request, 'performance_reviews/review_detail.html', {
        'review': review,
        'feedback': feedback
    })

@login_required
def edit_feedback(request, pk):
    """Edit or create feedback for a completed review"""
    review = get_object_or_404(ReviewSchedule, pk=pk)
    
    # Check permissions
    if not (request.user.is_hr or request.user == review.department_head):
        return HttpResponseForbidden("You don't have permission to edit feedback.")
    
    feedback, created = ReviewFeedback.objects.get_or_create(review=review)
    
    if request.method == 'POST':
        form = ReviewFeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            if form.cleaned_data['is_published']:
                review.status = 'completed'
                review.save()
                messages.success(request, 'Feedback published successfully!')
            else:
                messages.success(request, 'Feedback saved as draft.')
            return redirect('review_detail', pk=review.pk)
    else:
        form = ReviewFeedbackForm(instance=feedback)
    
    return render(request, 'performance_reviews/edit_feedback.html', {
        'form': form,
        'review': review
    })

@login_required
def employee_feedback(request, pk):
    """Allow employee to provide self-assessment before review"""
    review = get_object_or_404(ReviewSchedule, pk=pk)
    
    # Ensure only the employee can access their feedback form
    if request.user != review.employee:  # Changed from review.employee.user
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    feedback, created = ReviewFeedback.objects.get_or_create(review=review)
    
    if request.method == 'POST':
        # Only update the employee_feedback field
        feedback.employee_feedback = request.POST.get('employee_feedback')
        feedback.save()
        messages.success(request, 'Your feedback has been submitted.')
        return redirect('review_detail', pk=review.pk)
    
    return render(request, 'performance_reviews/employee_feedback.html', {
        'review': review,
        'feedback': feedback
    })