from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [

            'domain',
            'location',
            'joining',
            'compensation',
            'responsibilities',
            'learning_exposure',
            'ideal_candidate',
            'additional_notes',
        ]

        widgets = {
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'learning_exposure': forms.Textarea(attrs={'rows': 4}),
            'ideal_candidate': forms.Textarea(attrs={'rows': 4}),
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }
