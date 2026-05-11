from django.urls import path
from . import views

app_name = 'candidate'

urlpatterns = [
    path('onboarding/', views.dynamic_onboarding_view, name='onboarding'),
    path('dashboard/', views.candidate_dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/edit/<str:section>/', views.profile_edit, name='profile_edit_section'),
    path('profile/', views.profile_detail_view, name='profile_detail'),
    path('upgrade-status/', views.upgrade_status, name='upgrade_status'),
    path('pending_approval/', views.pending_approval, name='pending_approval'),

    path('profile/view/<str:username>/', views.candidate_public_profile, name='candidate_public_profile'),
]

