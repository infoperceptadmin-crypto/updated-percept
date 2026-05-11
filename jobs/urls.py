from django.urls import path
from . import views

urlpatterns = [

    # ================= DASHBOARD =================
    path('dashboard/', views.employer_analytics_dashboard, name='company_dashboard'),

    # ================= JOB POSTING =================
    path('', views.post_job, name='post_job'),
    path('jobs/manage/', views.manage_jobs, name='manage_jobs'),
    path('browse/', views.browse_jobs, name='browse_jobs'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    # ================= EDIT / DELETE JOB =================
    path('jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),

    # ================= APPLICANTS =================
    path('jobs/<int:job_id>/applicants/', views.manage_applicants, name='manage_applicants'),
    path('applications/update/<int:app_id>/<str:status>/', views.update_application_status, name='update_application_status'),


]
