from django.urls import path
from .views import dashboard, upload, home, signup

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload/', upload, name='upload'),
    path('accounts/signup/', signup, name='signup'),
]
