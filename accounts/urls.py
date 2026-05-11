from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_candidate, name='register_candidate'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]