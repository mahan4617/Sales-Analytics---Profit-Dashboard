from django.urls import path
from .views import upload_sales, upload_history, view_upload

urlpatterns = [
    path('upload/', upload_sales, name='upload_sales'),
    path('history/', upload_history, name='upload_history'),
    path('view/<str:source>/<int:pk>/', view_upload, name='view_upload'),
]
