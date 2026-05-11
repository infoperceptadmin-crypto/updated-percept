from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    # =========================
    # AUTH & DASHBOARD
    # =========================
    path('', views.admin_dashboard, name='admin_dashboard'),

    # =========================
    # VERIFY EMPLOYERS MAIN
    # =========================
    path('verify-employers/', views.verify_employers, name='verify_employers'),

    # =========================
    # FIRMS VERIFICATION
    # =========================
    path('verify-firms/', views.verify_firm, name='verify_firm'),
    path('firm/detail/<int:firm_id>/', views.view_firm_detail, name='view_firm_detail'),
    path('firm/<int:firm_id>/<str:action>/', views.update_firm_status, name='update_firm_status'),

    # =========================
    # CORPORATES VERIFICATION
    # =========================
    path('verify-corporates/', views.verify_corporate, name='verify_corporate'),
    path('corporate/detail/<int:corporate_id>/', views.view_corporate_detail, name='view_corporate_detail'),
    path('corporate/<int:corporate_id>/<str:action>/', views.update_corporate_status, name='update_corporate_status'),

    # =========================
    # CANDIDATES VERIFICATION (NEW)
    # =========================
    path('verify-candidates/', views.verify_candidate, name='verify_candidates'),
    path('candidate/detail/<int:candidate_id>/', views.view_candidate_detail, name='view_candidate_detail'),
    path('candidate/<int:candidate_id>/<str:action>/', views.update_candidate_status, name='update_candidate_status'),

    # =========================
    # SKILL CRUD
    # =========================
    path('manage-skills/', views.skill_list, name='manage_skills'),
    path('skill/add/', views.skill_add, name='manage_skill_add'),
    path('skill/edit/<int:id>/', views.skill_edit, name='manage_skill_edit'),
    path('skill/delete/<int:id>/', views.skill_delete, name='manage_skill_delete'),

    # =========================
    # DOMAIN CRUD
    # =========================
    path('domain/add/', views.domain_add, name='domain_add'),
    path('domain/edit/<int:id>/', views.domain_edit, name='domain_edit'),
    path('domain/delete/<int:id>/', views.domain_delete, name='domain_delete'),

    # =========================
    # EXPORT EXCEL ROUTES (NEW)
    # =========================
    path('export/skills/', views.export_skills_excel, name='export_skills_excel'),

    path('export/firm/<int:firm_id>/', views.export_single_firm_excel, name='export_single_firm'),
    path('export/firms/', views.export_all_firms_excel, name='export_all_firms'),

    path('export/corporate/<int:corporate_id>/', views.export_single_corporate_excel, name='export_single_corporate'),
    path('export/corporates/', views.export_all_corporates_excel, name='export_all_corporates'),

    path('export/candidate/<int:candidate_id>/', views.export_single_candidate_excel, name='export_single_candidate'),
    path('export/candidates/', views.export_all_candidates_excel, name='export_all_candidates'),
]