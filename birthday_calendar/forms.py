
from django import forms
from .models import BirthdayWish

class BirthdayWishForm(forms.ModelForm):
    class Meta:
        model = BirthdayWish
        fields = ['employee', 'message', 'description', 'celebration_style', 'display_on_dashboard']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure display_on_dashboard is checked by default
        self.fields['display_on_dashboard'].initial = True
