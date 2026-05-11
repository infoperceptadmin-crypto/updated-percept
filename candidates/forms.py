from django import forms
from django.forms import inlineformset_factory
from adminpanel.models import ManageSkill, Domain
from .models import (
    CandidateProfile, CandidateSkill,
    Education, Experience, Achievement,
    IndustryChoices, LanguageChoices, ProficiencyChoices
)


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget = self.fields[field].widget

            if not isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.SelectMultiple)):
                widget.attrs.update({'class': 'form-control'})

            if isinstance(widget, forms.SelectMultiple):
                widget.attrs.update({'class': 'form-select choices-multiple'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        if 'software_skills' in self.cleaned_data:
            selected_skills = self.cleaned_data['software_skills']
            CandidateSkill.objects.filter(candidate=instance).delete()
            new_skills = [
                CandidateSkill(candidate=instance, skill=skill, proficiency=ProficiencyChoices.BEGINNER)
                for skill in selected_skills
            ]
            CandidateSkill.objects.bulk_create(new_skills)

        if commit:
            self.save_m2m()
        return instance


SEARCHABLE_MULTI_WIDGET = forms.SelectMultiple(attrs={'class': 'choices-multiple'})

# ==========================================
# CA TRACK PROFILE FORMS
# ==========================================

class FoundationProfileForm(StyledModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['bio', 'cv_template_preference', 'icai_reg_num', 'languages', 'availability',
                  'foundation_year', 'foundation_attempts', 'software_skills']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'languages': SEARCHABLE_MULTI_WIDGET,
            'software_skills': SEARCHABLE_MULTI_WIDGET,
        }

class InterProfileForm(StyledModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['bio', 'cv_template_preference', 'icai_reg_num', 'languages', 'availability',
                  'inter_attempts_g1', 'inter_attempts_g2', 'preferred_articleship_city',
                  'preferred_industries', 'preferred_domains', 'software_skills']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'languages': SEARCHABLE_MULTI_WIDGET,
            'preferred_industries': SEARCHABLE_MULTI_WIDGET,
            'preferred_domains': SEARCHABLE_MULTI_WIDGET,
            'software_skills': SEARCHABLE_MULTI_WIDGET,
        }

class OngoingProfileForm(StyledModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['bio', 'cv_template_preference', 'icai_reg_num', 'languages', 'availability',
                  'current_firm_city', 'articleship_start_date', 'seeking_type', 'is_confidential_mode',
                  'preferred_industries', 'preferred_domains', 'software_skills']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'languages': SEARCHABLE_MULTI_WIDGET,
            'articleship_start_date': forms.DateInput(attrs={'type': 'date'}),
            'preferred_industries': SEARCHABLE_MULTI_WIDGET,
            'preferred_domains': SEARCHABLE_MULTI_WIDGET,
            'software_skills': SEARCHABLE_MULTI_WIDGET,
        }

class CompletedProfileForm(StyledModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['bio', 'cv_template_preference', 'icai_reg_num', 'languages', 'availability',
                  'articleship_end_date', 'domain_exposure', 'preferred_job_roles', 'employment_type',
                  'preferred_industries', 'preferred_domains', 'software_skills']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'languages': SEARCHABLE_MULTI_WIDGET,
            'articleship_end_date': forms.DateInput(attrs={'type': 'date'}),
            'preferred_industries': SEARCHABLE_MULTI_WIDGET,
            'preferred_domains': SEARCHABLE_MULTI_WIDGET,
            'software_skills': SEARCHABLE_MULTI_WIDGET,
        }

class FinalProfileForm(StyledModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['bio', 'cv_template_preference', 'icai_reg_num', 'languages', 'availability',
                  'final_group_appeared', 'final_attempts', 'career_preference', 'study_status',
                  'preferred_industries', 'preferred_domains', 'software_skills']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'languages': SEARCHABLE_MULTI_WIDGET,
            'preferred_industries': SEARCHABLE_MULTI_WIDGET,
            'preferred_domains': SEARCHABLE_MULTI_WIDGET,
            'software_skills': SEARCHABLE_MULTI_WIDGET,
        }


# ==========================================
# ✅ COMMERCE GRADUATE PROFILE FORM
# ==========================================
class CommerceGradProfileForm(StyledModelForm):
    class Meta:
        model = CandidateProfile
        # Completely omits ICAI Reg Num, Articleship details, and CA attempts
        fields = [
            'bio',
            'cv_template_preference',
            'languages',
            'availability',
            'preferred_job_roles',
            'employment_type',
            'preferred_industries',
            'preferred_domains',
            'software_skills'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a short professional summary...'}),
            'languages': SEARCHABLE_MULTI_WIDGET,
            'preferred_industries': SEARCHABLE_MULTI_WIDGET,
            'preferred_domains': SEARCHABLE_MULTI_WIDGET,
            'software_skills': SEARCHABLE_MULTI_WIDGET,
        }


# ==========================================
# DYNAMIC FORMSETS (Shared by all)
# ==========================================
class EducationForm(StyledModelForm):
    class Meta:
        model = Education
        fields = ['qualification_name', 'institution_board', 'passing_year', 'score_percentage', 'remarks']


class ExperienceForm(StyledModelForm):
    class Meta:
        model = Experience
        fields = ['designation', 'company_firm_name', 'location', 'start_date', 'end_date', 'is_currently_working',
                  'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Enter key responsibilities using bullet points...'}),
            'is_currently_working': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class AchievementForm(StyledModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'issuer_organization', 'year', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2})
        }


EducationFormSet = inlineformset_factory(CandidateProfile, Education, form=EducationForm, extra=1, can_delete=True)
ExperienceFormSet = inlineformset_factory(CandidateProfile, Experience, form=ExperienceForm, extra=1, can_delete=True)
AchievementFormSet = inlineformset_factory(CandidateProfile, Achievement, form=AchievementForm, extra=1,
                                           can_delete=True)

# from django import forms
# from django.forms import inlineformset_factory
# from adminpanel.models import ManageSkill, Domain
# from .models import (
#     CandidateProfile, CandidateSkill,
#     Education, Experience, Achievement,
#     IndustryChoices, LanguageChoices, ProficiencyChoices
# )
#
#
# class StyledModelForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             widget = self.fields[field].widget
#
#             if not isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.SelectMultiple)):
#                 widget.attrs.update({'class': 'form-control'})
#
#             if isinstance(widget, forms.SelectMultiple):
#                 widget.attrs.update({'class': 'form-select choices-multiple'})
#
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         if commit:
#             instance.save()
#
#         if 'software_skills' in self.cleaned_data:
#             selected_skills = self.cleaned_data['software_skills']
#             CandidateSkill.objects.filter(candidate=instance).delete()
#             new_skills = [
#                 CandidateSkill(candidate=instance, skill=skill, proficiency=ProficiencyChoices.BEGINNER)
#                 for skill in selected_skills
#             ]
#             CandidateSkill.objects.bulk_create(new_skills)
#
#         if commit:
#             self.save_m2m()
#         return instance
#
#
# SEARCHABLE_MULTI_WIDGET = forms.SelectMultiple(attrs={'class': 'choices-multiple'})
#
#
# # ==========================================
# # BASE PROFILE FORMS (Level 1 to 5)
# # ==========================================
#
# class FoundationProfileForm(StyledModelForm):
#     software_skills = forms.ModelMultipleChoiceField(queryset=ManageSkill.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                      required=False)
#     languages = forms.MultipleChoiceField(choices=LanguageChoices.choices, widget=SEARCHABLE_MULTI_WIDGET,
#                                           required=False)
#     preferred_domains = forms.ModelMultipleChoiceField(queryset=Domain.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                        required=False, label="Preferred Domains (For Job Matches)")
#
#     class Meta:
#         model = CandidateProfile
#         fields = ['foundation_year', 'foundation_attempts', 'icai_reg_num', 'languages', 'software_skills',
#                   'preferred_domains', 'bio', 'cv_template_preference']
#         widgets = {'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Professional summary...'})}
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['icai_reg_num'].required = False
#
#     def clean_languages(self):
#         return self.cleaned_data.get('languages', [])
#
#
# class InterProfileForm(StyledModelForm):
#     preferred_domains = forms.ModelMultipleChoiceField(queryset=Domain.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                        required=False, label="Preferred Domains (For Job Matches)")
#     preferred_industries = forms.MultipleChoiceField(choices=IndustryChoices.choices, widget=SEARCHABLE_MULTI_WIDGET,
#                                                      required=False)
#     software_skills = forms.ModelMultipleChoiceField(queryset=ManageSkill.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                      required=False)
#     languages = forms.MultipleChoiceField(choices=LanguageChoices.choices, widget=SEARCHABLE_MULTI_WIDGET,
#                                           required=False)
#
#     class Meta:
#         model = CandidateProfile
#         fields = ['foundation_year', 'foundation_attempts', 'inter_attempts_g1', 'inter_attempts_g2', 'icai_reg_num',
#                   'preferred_articleship_city', 'availability', 'preferred_domains', 'preferred_industries',
#                   'software_skills', 'languages', 'bio', 'cv_template_preference']
#         widgets = {'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Professional summary...'})}
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['icai_reg_num'].required = False
#         self.fields['inter_attempts_g2'].label = "Intermediate Group 2 Attempts"
#
#     def clean_preferred_industries(self):
#         return self.cleaned_data.get('preferred_industries', [])
#
#     def clean_languages(self):
#         return self.cleaned_data.get('languages', [])
#
#
# class OngoingProfileForm(StyledModelForm):
#     software_skills = forms.ModelMultipleChoiceField(queryset=ManageSkill.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                      required=False)
#     languages = forms.MultipleChoiceField(choices=LanguageChoices.choices, widget=SEARCHABLE_MULTI_WIDGET,
#                                           required=False)
#     preferred_domains = forms.ModelMultipleChoiceField(queryset=Domain.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                        required=False, label="Preferred Domains (For Job Matches)")
#
#     class Meta:
#         model = CandidateProfile
#         fields = ['foundation_year', 'foundation_attempts', 'inter_attempts_g1', 'inter_attempts_g2',
#                   'articleship_start_date', 'current_firm_city', 'seeking_type', 'is_confidential_mode', 'icai_reg_num',
#                   'software_skills', 'languages', 'preferred_domains', 'bio', 'cv_template_preference']
#         widgets = {
#             'articleship_start_date': forms.DateInput(attrs={'type': 'date'}),
#             'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Professional summary...'})
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['icai_reg_num'].required = False
#         self.fields['inter_attempts_g2'].label = "Intermediate Group 2 Attempts"
#
#     def clean_languages(self):
#         return self.cleaned_data.get('languages', [])
#
#
# class CompletedProfileForm(StyledModelForm):
#     domain_exposure = forms.ModelMultipleChoiceField(queryset=Domain.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                      required=False, label="Domains Worked In (Past Experience)")
#     preferred_domains = forms.ModelMultipleChoiceField(queryset=Domain.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                        required=False,
#                                                        label="Preferred Domains (For Future Job Matches)")
#     software_skills = forms.ModelMultipleChoiceField(queryset=ManageSkill.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                      required=False)
#     languages = forms.MultipleChoiceField(choices=LanguageChoices.choices, widget=SEARCHABLE_MULTI_WIDGET,
#                                           required=False)
#
#     class Meta:
#         model = CandidateProfile
#         fields = ['foundation_year', 'foundation_attempts', 'inter_attempts_g1', 'inter_attempts_g2',
#                   'articleship_start_date', 'articleship_end_date', 'domain_exposure', 'preferred_domains',
#                   'preferred_job_roles', 'employment_type', 'availability', 'icai_reg_num', 'software_skills',
#                   'languages', 'articleship_completion_cert', 'experience_proof', 'bio', 'cv_template_preference']
#         widgets = {
#             'articleship_start_date': forms.DateInput(attrs={'type': 'date'}),
#             'articleship_end_date': forms.DateInput(attrs={'type': 'date'}),
#             'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Professional summary...'})
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['icai_reg_num'].required = True
#
#     def clean_domain_exposure(self):
#         selected_domains = self.cleaned_data.get('domain_exposure', [])
#         return [domain.domain_name for domain in selected_domains]
#
#     def clean_languages(self):
#         return self.cleaned_data.get('languages', [])
#
#
# class FinalProfileForm(StyledModelForm):
#     domain_exposure = forms.ModelMultipleChoiceField(queryset=Domain.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                      required=False, label="Domains Worked In (Articleship)")
#     preferred_domains = forms.ModelMultipleChoiceField(queryset=Domain.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                        required=False, label="Preferred Domains (For Job Matches)")
#     software_skills = forms.ModelMultipleChoiceField(queryset=ManageSkill.objects.all(), widget=SEARCHABLE_MULTI_WIDGET,
#                                                      required=False)
#     languages = forms.MultipleChoiceField(choices=LanguageChoices.choices, widget=SEARCHABLE_MULTI_WIDGET,
#                                           required=False)
#
#     class Meta:
#         model = CandidateProfile
#         fields = ['foundation_year', 'foundation_attempts', 'inter_attempts_g1', 'inter_attempts_g2',
#                   'articleship_end_date', 'domain_exposure', 'preferred_domains', 'final_group_appeared',
#                   'final_attempts', 'icai_reg_num', 'career_preference', 'study_status', 'software_skills', 'languages',
#                   'bio', 'cv_template_preference']
#         widgets = {
#             'articleship_end_date': forms.DateInput(attrs={'type': 'date'}),
#             'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Professional summary...'})
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['icai_reg_num'].required = False
#
#     def clean_domain_exposure(self):
#         selected_domains = self.cleaned_data.get('domain_exposure', [])
#         return [domain.domain_name for domain in selected_domains]
#
#     def clean_languages(self):
#         return self.cleaned_data.get('languages', [])
#
#
# # ==========================================
# # MULTI-ROW FORMSETS (Education, Experience, Achievement)
# # ==========================================
# class EducationForm(StyledModelForm):
#     class Meta:
#         model = Education
#         fields = ['qualification_name', 'institution_board', 'passing_year', 'score_percentage', 'remarks']
#
#
# class ExperienceForm(StyledModelForm):
#     class Meta:
#         model = Experience
#         fields = ['designation', 'company_firm_name', 'location', 'start_date', 'end_date', 'is_currently_working',
#                   'description']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#             'end_date': forms.DateInput(attrs={'type': 'date'}),
#             'description': forms.Textarea(
#                 attrs={'rows': 4, 'placeholder': 'Enter key responsibilities using bullet points...'}),
#             'is_currently_working': forms.CheckboxInput(attrs={'class': 'form-check-input'})
#         }
#
#
# class AchievementForm(StyledModelForm):
#     class Meta:
#         model = Achievement
#         fields = ['title', 'issuer_organization', 'year', 'description']
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 2})
#         }
#
#
# EducationFormSet = inlineformset_factory(CandidateProfile, Education, form=EducationForm, extra=1, can_delete=True)
# ExperienceFormSet = inlineformset_factory(CandidateProfile, Experience, form=ExperienceForm, extra=1, can_delete=True)
# AchievementFormSet = inlineformset_factory(CandidateProfile, Achievement, form=AchievementForm, extra=1,
#                                            can_delete=True)
