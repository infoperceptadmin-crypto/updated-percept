from django.urls import path
from . import views

urlpatterns = [
    path("matched-jobs/", views.matched_jobs, name="matched_jobs"),
]
