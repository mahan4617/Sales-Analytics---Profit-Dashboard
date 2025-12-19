from django.urls import path
from .views import analyze_latest, analysis_dashboard, analyze_file

urlpatterns = [
    path('', analyze_latest, name='analyze_latest'),
    path('dashboard/', analysis_dashboard, name='analysis_dashboard'),
    path('<str:source>/<int:pk>/', analyze_file, name='analyze_file'),
]
