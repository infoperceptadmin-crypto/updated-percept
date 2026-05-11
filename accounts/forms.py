from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CandidateRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email ID'}))
    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit Mobile'}))
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred Work Location'}))

    candidate_status = forms.ChoiceField(
        choices=User.CAStatus.choices,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_ca_status'})
    )

    inter_group_status = forms.ChoiceField(
        choices=User.InterGroupStatus.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_inter_group_status'})
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'mobile_number', 'city', 'candidate_status', 'inter_group_status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['password1', 'password2']:
            if field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
                self.fields[
                    field].help_text = None

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if len(mobile) != 10 or not mobile.isdigit():
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        return mobile