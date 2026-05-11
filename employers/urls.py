from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

path('firm/dashboard/', views.firm_dashboard, name='firm_dashboard'),
    path('corporate/dashboard/', views.corporate_dashboard, name='corporate_dashboard'),
path('reg_choice/', views.register_choice, name='register_choice'),

# FIRM
path('firm/register/', views.firm_register, name='firm_register'),
path('firm/profile/<int:firm_id>/', views.firm_profile, name='firm_profile'),
path('pending_approval/', views.pending_approval, name='pending_approval'),


# CORPORATE
path('corporate/register/', views.corporate_register, name='corporate_register'),
path('corporate/profile/<int:corporate_id>/', views.corporate_profile, name='corporate_profile'),


]
