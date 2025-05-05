from django import forms
from .models import ReviewSchedule, ReviewFeedback

class ReviewScheduleForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Schedule the review meeting"
    )
    
    class Meta:
        model = ReviewSchedule
        fields = ['employee', 'department_head', 'title', 'description', 'scheduled_date']

class ReviewFeedbackForm(forms.ModelForm):
    class Meta:
        model = ReviewFeedback
        fields = ['employee_feedback', 'department_head_feedback', 'strengths', 
                  'areas_for_improvement', 'goals', 'final_rating', 'is_published']
        widgets = {
            'employee_feedback': forms.Textarea(attrs={'rows': 4}),
            'department_head_feedback': forms.Textarea(attrs={'rows': 4}),
            'strengths': forms.Textarea(attrs={'rows': 4}),
            'areas_for_improvement': forms.Textarea(attrs={'rows': 4}),
            'goals': forms.Textarea(attrs={'rows': 4}),
        }